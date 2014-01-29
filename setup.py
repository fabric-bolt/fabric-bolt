#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'django>=1.5,<1.6',
    'django-compressor',
    'django-grappelli',
    'south',
    'PIL',
    'django-stronghold',
    'django-crispy-forms',
    'django-custom-user',
    'django-tables2',
    'django-braces',
    'django-sekizai',
    'fabric',
    'logan',
]

dev_requires = [
    'django_debug_toolbar',
    'django-debug-toolbar-template-timings',
    'mock',
]

postgres_requires = [
    'psycopg2',
]

mysql_requires = [
    'MySQL-python',
]


setup(
    name='fabric-bolt',
    version='0.0.1',
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