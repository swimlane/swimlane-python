import glob
import os
import subprocess
import tempfile
import zipfile

print('Extracting packages')

zip_file = zipfile.ZipFile(os.path.dirname(__file__))
temp_dir = tempfile.mkdtemp()
zip_file.extractall(temp_dir)
os.chdir(temp_dir)

#print('Installing virtualenv')
#
#virtualenv_wheel = glob.glob(os.path.join('.', 'deps', 'virtualenv*'))[0]
#
#subprocess.check_call(['pip', 'install', '--no-index', '--no-deps', '--upgrade', '--force-reinstall', '--find-links=.', virtualenv_wheel])
#
#import virtualenv
#
#print('Creating shim env')
#
#venv_dir = os.path.join(os.path.expanduser('~'), '.swimlane-shim')
#virtualenv.create_environment(venv_dir)

print('Installing swimlane driver')

#venv_pip = os.path.join(venv_dir, 'Scripts', 'pip.exe')
paths = glob.glob(os.path.join('.', 'deps', '*'))
subprocess.check_call(['python', '-m', 'pip', 'install', '--no-index', '--no-deps', '--upgrade', '--force-reinstall', '--find-links=.'] + paths)

shim_code = '''
import os

def activate_shim_env(venv_dir):
    activate_file = os.path.join(venv_dir, 'Scripts', 'activate_this.py')
    with open(activate_file) as f:
        exec(f.read(), {'__file__': activate_file})
        
'''

'''
print('\n'.join([
    '==========',
    'To activate new swimlane driver shim, copy following code block to top of task scripts',
    '==========',
    shim_code,
    'activate_shim_env({!r})'.format(venv_dir),
    'import swimlane',
    '',
    '=========='
]))
'''
