from setuptools import setup, find_packages
from get_requirements import get_requirements

setup(
    name='face-rec-backend',
    version='0.1',
    author='Jai Swarup',
    author_email='jaiswarup0@gmail.com',
    packages=find_packages(),
    install_requires=[get_requirements('requirements.txt')],

)