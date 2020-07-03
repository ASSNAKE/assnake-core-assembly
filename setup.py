from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

from assnake_core_assembly import snake_module

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        snake_module.deploy_module()
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        snake_module.deploy_module()
        install.run(self)

setup(
    name='assnake-core-assembly',
    version='0.0.2',
    packages=find_packages(),
    entry_points = {
        'assnake.plugins': ['assnake-core-assembly = assnake_core_assembly:snake_module']
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)