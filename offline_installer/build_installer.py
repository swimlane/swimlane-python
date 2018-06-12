"""Creates dist/swimlane-python-offline-installer-<platform>-<py_version>.pyz offline driver installer archives"""
import glob
import os
import tempfile
import shutil
import subprocess
from zipfile import ZipFile

import sys

# Map readable platform name to pip / .whl platform value
PY_PLATFORMS = {
    'windows': 'win_amd64',
    'linux': 'manylinux1_x86_64'
}

# Python configs
PY_VERSION = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
PY_PLATFORM = PY_PLATFORMS['windows']

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



ALL_DEPS_DIR = tempfile.mkdtemp()
CACHE_DIR = tempfile.mkdtemp()

# Build local wheel
print('Building swimlane wheel')
os.chdir(os.path.join(ROOT_DIR, '..'))
subprocess.check_call(
    r'''
    pip \
    --cache-dir="{cache_dir}" \
    wheel \
    --no-deps \
    -w "{deps_dir}" \
    .
    '''.format(
        deps_dir=ALL_DEPS_DIR,
        cache_dir=CACHE_DIR
    ),
    shell=True
)
swimlane_whl = glob.glob(os.path.join(ALL_DEPS_DIR, 'swimlane-*'))[0]
swimlane_version = swimlane_whl.split('/')[-1].split('-')[1]
print('Built swimlane version ' + swimlane_version)

# Collect and build all dependencies

print('Downloading all dependencies to {}'.format(ALL_DEPS_DIR))

os.chdir(ALL_DEPS_DIR)

# Initial pass to recursively grab all deps, regardless of platform support
subprocess.check_call(
    r'''
    pip \
    --cache-dir="{cache_dir}" \
    download -r {requirements} \
    '''.format(
        cache_dir=CACHE_DIR,
        requirements=os.path.join(ROOT_DIR, '..', 'requirements.txt')
    ),
    shell=True
)

ZIPAPP_DIR = tempfile.mkdtemp()

REAL_DEPS_DIR = os.path.join(ZIPAPP_DIR, 'deps')
os.mkdir(REAL_DEPS_DIR)
os.chdir(REAL_DEPS_DIR)

print('Collecting real dependencies to {}'.format(REAL_DEPS_DIR))

for f in os.listdir(ALL_DEPS_DIR):

    filename = os.path.join(ALL_DEPS_DIR, f)

    if f.endswith('.tar.gz'):
        f = f[:-7]

    name, version = f.rsplit('-', 4)[:2]
    package = '=='.join([name, version])

    # Try to download platform-specific wheel
    try:
        abi_extension = 'mu' if PY_PLATFORM == 'manylinux1_x86_64' else 'm'
        subprocess.check_call(
            r'''
            pip --cache-dir="{cache_dir}" download \
            --no-deps \
            --platform={platform} \
            --python-version={version} \
            --abi=cp{version}{abi_extension} \
            --only-binary=:all: \
            {package}
            '''.format(
                cache_dir=CACHE_DIR,
                platform=PY_PLATFORM,
                abi_extension=abi_extension,
                version=PY_VERSION,
                package=package
            ),
            shell=True
        )
    except Exception:
        # Non-zero exit code, package not available as a platform-specific wheel, just copy in tar file as dep
        shutil.copy(filename, REAL_DEPS_DIR)

print('Collected dependencies to {}'.format(REAL_DEPS_DIR))

# Create self-extracting zip installer

print('Creating self-installing zip')
DIST_DIR = os.path.join(ROOT_DIR, '..', 'dist')
if not os.path.isdir(DIST_DIR):
    os.mkdir(DIST_DIR)

zippath = os.path.realpath(os.path.join(
    DIST_DIR,
    'swimlane-python-{version}-offline-installer-{platform}-py{py_version}.pyz'.format(
        version=swimlane_version,
        platform=PY_PLATFORM,
        py_version=PY_VERSION
    )
))

if os.path.exists(zippath):
    os.remove(zippath)

with ZipFile(zippath, 'w') as zipf:
    zipf.write(os.path.join(ROOT_DIR, '__main__.py'), '__main__.py')

    for f in os.listdir(REAL_DEPS_DIR):
        print('Adding file "{}"'.format(f))
        zipf.write(os.path.join(REAL_DEPS_DIR, f), os.path.join('deps', f))

print('Offline installer written to {}'.format(zippath))
