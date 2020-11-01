"""Creates dist/swimlane-python-offline-installer-<platform>-<py_version>.pyz offline driver installer archives
based on the platform it is run. Not to be used as a builder for different platform. For proper matrix builds."""
import glob
import os
import tempfile
import shutil
import subprocess
import platform
import sys

from zipfile import ZipFile
from os import path


PY_VERSION = '{}{}'.format(sys.version_info.major, sys.version_info.minor)
PY_PLATFORM = 'win_amd64' if platform.system() == 'Windows' else 'linux_x86_64'
ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
ALL_DEPS_DIR = tempfile.mkdtemp()
CACHE_DIR = tempfile.mkdtemp()

os.chdir(ROOT_DIR)
cmd = 'pip --cache-dir="{cache}" wheel --no-deps -w "{deps_dir}" .'.format(deps_dir=ALL_DEPS_DIR, cache=CACHE_DIR)
subprocess.check_call(cmd, stdout=subprocess.DEVNULL, shell=True)
swimlane_whl = glob.glob(path.join(ALL_DEPS_DIR, 'swimlane-*'))[0]
swimlane_version = swimlane_whl.split('/')[-1].split('-')[1]

os.chdir(ALL_DEPS_DIR)
cmd = 'pip --cache-dir="{cache_dir}"  download -r {requirements} --prefer-binary'\
    .format(cache_dir=CACHE_DIR, requirements=path.join(ROOT_DIR, 'requirements.txt'))
subprocess.check_call(cmd, stdout=subprocess.DEVNULL, shell=True)

DIST_DIR = path.join(ROOT_DIR, 'dist')
if not path.isdir(DIST_DIR):
    os.mkdir(DIST_DIR)

zip_file_name = 'swimlane-python-{version}-offline-installer-{platform}-py{py_version}.pyz'\
    .format(version=swimlane_version, platform=PY_PLATFORM, py_version=PY_VERSION)
zip_path = path.realpath(path.join(DIST_DIR, zip_file_name))

if os.path.exists(zip_path):
    os.remove(zip_path)

with ZipFile(zip_path, 'w') as zip_file:
    zip_file.write(path.join(ROOT_DIR, 'offline_installer', '__main__.py'), '__main__.py')
    for f in os.listdir(ALL_DEPS_DIR):
        zip_file.write(path.join(ALL_DEPS_DIR, f), path.join('deps', f))

print(zip_file_name)

shutil.rmtree(ALL_DEPS_DIR, ignore_errors=True)
shutil.rmtree(CACHE_DIR, ignore_errors=True)
