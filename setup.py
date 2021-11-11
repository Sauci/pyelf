import os.path

from setuptools import setup

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'VERSION')), 'r') as fp:
    version = fp.read().splitlines()[0]

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.md')), 'r') as fp:
    long_description = fp.read()

setup(
    name='sauci-pyelf',
    version=version,
    packages=['pyelf'],
    url='https://github.com/Sauci/pyelf',
    license='MIT',
    author='Guillaume Sottas',
    author_email='guillaumesottas@gmail.com',
    description='high level API to retrieve information from ELF files.',
    long_description=long_description,
    install_requires=['pyelftools'],
    entry_points={
        'console_scripts': ['pyelf=pyelf:main']
    },
)
