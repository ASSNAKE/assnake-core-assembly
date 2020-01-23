from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from assnake.utils import get_config_loc, load_config_file
import os, shutil

def prepare_params():
    if os.path.isfile(get_config_loc()):
        config = load_config_file()
        os.makedirs(os.path.join(config['assnake_db'], 'params/megahit'), exist_ok=True)
        shutil.copyfile('./assnake_core_assembly/megahit/def.json', os.path.join(config['assnake_db'], 'params/megahit/def.json'))

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        prepare_params()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        prepare_params()
        install.run(self)

setup(
    name='assnake-core-assembly',
    version='0.0.1',
    packages=find_packages(),
    entry_points = {
        'assnake.plugins': ['assnake-core-assembly = assnake_core_assembly.snake_module_setup:snake_module']
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)