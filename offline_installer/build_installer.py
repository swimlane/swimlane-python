"""Creates dist/swimlane-python-offline-installer-win_amd64-<py_version>.zip offline driver installer for windows"""

import os
import tempfile
import shutil
from zipfile import ZipFile

import sys
from pip import main as pipmain

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)

ALL_DEPS_DIR = tempfile.mkdtemp()
os.chdir(ALL_DEPS_DIR)


# Python configs
PY_VERSION = 'py{}{}'.format(sys.version_info.major, sys.version_info.minor)
PY_PLATFORM = 'win_amd64'


# Collect and build all dependencies

print('Downloading all dependencies to {}'.format(ALL_DEPS_DIR))

# Initial pass to recursively grab all deps, regardless of platform support
pipmain(['download', '-r', os.path.join(ROOT_DIR, '..', 'requirements.txt')])

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

    # Try to download Windows-platform wheel
    if pipmain([
        'download',
        '--no-deps',
        '--platform={}'.format(PY_PLATFORM),
        '--only-binary=:all:',
        package
    ]):
        # Non-zero exit code, package not available as a Windows wheel, just copy in tar file as dep
        shutil.copy(filename, REAL_DEPS_DIR)

print('Collected dependencies to {}'.format(REAL_DEPS_DIR))


# Create self-extracting zip installer

print('Creating self-installing zip')
DIST_DIR = os.path.join(ROOT_DIR, '..', 'dist')
if not os.path.isdir(DIST_DIR):
    os.mkdir(DIST_DIR)

zippath = os.path.join(DIST_DIR, 'swimlane-python-offline-installer-{platform}-{py_version}.pyz'.format(
    platform=PY_PLATFORM,
    py_version=PY_VERSION
))
if os.path.exists(zippath):
    os.remove(zippath)

with ZipFile(zippath, 'w') as zipf:

    zipf.write(os.path.join(ROOT_DIR, '__main__.py'), '__main__.py')

    for f in os.listdir(REAL_DEPS_DIR):
        zipf.write(os.path.join(REAL_DEPS_DIR, f), os.path.join('deps', f))

print('Offline installer written to {}'.format(zippath))
