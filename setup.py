from setuptools import setup

setup(
    name='pyelf',
    version='0.1.0',
    packages=['pyelf'],
    url='',
    license='BSD',
    author='Guillaume Sottas',
    author_email='guillaumesottas@gmail.com',
    description='high level API to retrieve informations from ELF files.',
    install_requires=['pytest',
                      'pyelftools']
)
