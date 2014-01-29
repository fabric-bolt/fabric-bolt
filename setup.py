#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'django>=1.6,<1.7',
    'south>=0.8.4,<0.9',
    'pillow>=2.3.0,<2.4',
    'django-stronghold>=0.2.4,<0.3',
    'django-crispy-forms>=1.4.0,<1.5',
    'django-custom-user>=0.3,<0.4',
    'django-tables2>=0.14.0,<0.15',
    'django-braces>=1.3.1,<1.4',
    'django-sekizai>=0.7,<0.8',
    'fabric>=1.8.1,<1.9',
    'logan>=0.5.9,<0.6',
]

dev_requires = [
    'django_debug_toolbar>=1.0.1,<1.1',
    'django-grappelli>=2.5.1,<2.6',
    'django-debug-toolbar-template-timings>=0.5.5,<0.6',
    'mock>=1.0.1,<1.1',
]

postgres_requires = [
    'psycopg2>=2.5.2,<2.6',
]

mysql_requires = [
    'MySQL-python>=1.2.5,<1.3',
]


setup(
    name='fabric-bolt',
    version='0.0.2',
    author='Dan Dietz, Nathaniel Pardington, Jared Proffitt',
    url='https://github.com/worthwhile/fabric-bolt',
    description='A web interface to fabric deployments.',
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'dev': install_requires + dev_requires,
        'postgres': install_requires + postgres_requires,
        'mysql': install_requires + mysql_requires,
    },
    license='MIT',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fabric-bolt = fabric_bolt.utils.runner:main',
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python'
    ],
)