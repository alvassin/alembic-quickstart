import os
from importlib.machinery import SourceFileLoader

from setuptools import setup, find_packages


MODULE_NAME = 'staff'

module = SourceFileLoader(
    MODULE_NAME,
    os.path.join(MODULE_NAME, '__init__.py')
).load_module()


def load_requirements(file: str):
    """
    Load requirements from specified file.
    """
    with open(file, 'r') as f:
        for line in map(str.strip, f):
            if line.startswith('#'):
                continue
            if line.startswith('-r '):
                yield from load_requirements(line[3:])
            else:
                yield line


setup(
    name=MODULE_NAME,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    long_description=open('README.rst').read(),
    platforms="all",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    entry_points={
        'console_scripts': [
            'staff-api = staff.main:main',
            'staff-db = staff.db:main'
        ]
    },
    packages=find_packages(exclude=['tests']),
    package_data={
        MODULE_NAME: ['alembic.ini']
    },
    install_requires=load_requirements('requirements.txt'),
    python_requires=">3.5.*, <4",
    extras_require={
        'dev': load_requirements('requirements.dev.txt'),
    },
    url='https://github.com/alvassin/alembic-quickstart'
)