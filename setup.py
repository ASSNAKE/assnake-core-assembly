from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from assnake.utils import read_assnake_instance_config
import os, shutil

def prepare_params():
    instance_config = read_assnake_instance_config()
    if instance_config is not None:

        os.makedirs(os.path.join(instance_config['assnake_db'], 'params/megahit'), exist_ok=True)

        shutil.copyfile('./assnake_core_assembly/megahit/def.json', os.path.join(instance_config['assnake_db'], 'params/megahit/def.json'))

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
    version='0.0.2',
    packages=find_packages(),
    entry_points = {
        'assnake.plugins': ['assnake-core-assembly = assnake_core_assembly.snake_module_setup:snake_module']
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)