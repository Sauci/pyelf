from setuptools import setup

setup(
    name='pyelf',
    version='0.1.0',
    packages=['pyelf'],
    url='https://github.com/Sauci/pyelf',
    license='BSD',
    author='Guillaume Sottas',
    author_email='guillaumesottas@gmail.com',
    description='high level API to retrieve information from ELF files.',
    install_requires=['pyelftools'],
    entry_points={
        'console_scripts': ['pyelf=pyelf:main']
    },
)
