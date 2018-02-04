from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


REQUIREMENTS = ['tornado',
                ]


TEST_REQUIREMENTS = ['pytest-tornado',
                     ]


setup(
    name='conda-channel-browser',
    version='0.1dev0',
    description='A webapplication for browsing a conda channel',
    long_description=long_description,
    url='https://github.com/pelson/conda-channel-browser',
    author='Phil Elson',
    author_email='pelson.pub@gmail.com',
    keywords='conda channel web application',
    packages=find_packages(exclude=[]),
    python_requires='>=3.5',
    install_requires=REQUIREMENTS,
    extras_require={
        'test': TEST_REQUIREMENTS,
    },
)
