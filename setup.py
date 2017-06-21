#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'django==1.10.7',
    'pillow==4.1.0',
    'django-stronghold==0.2.8',
    'django-crispy-forms==1.6.1',
    'django-authtools==1.5.0',
    'django-tables2==1.4.2',
    'django-braces==1.11.0',
    'django-sekizai==0.10.0',
    'fabric==1.13.1',
    'logan==0.7.2',
    'django-bootstrap-form==3.2.1',
    'croniter==0.3.16',
    'GitPython==2.1.3',
    'django-graphos==0.3.41',
    'django-appconf==1.0.2',
    'django-activeurl==0.1.9',
    'requests==2.13.0',
    'virtualenv==15.1.0',
    'channels==1.1.3',
    'autobahn==0.18.1',
    'daphne==1.2.0',
    'six==1.10.0',
    'ansiconv==1.0.0',
    'pycrypto==2.6.1',
]

dev_requires = [
    'django-debug-toolbar==1.7',
    'django-debug-toolbar-template-timings==0.7',
    'mock==2.0.0',
    'model_mommy==1.3.2'
]

postgres_requires = [
    'psycopg2==2.7.1',
]

mysql_requires = [
    'MySQL-python==1.2.5',
]


setup(
    name='fabric-bolt',
    version='0.2b2',
    author='Dan Dietz, Nathaniel Pardington, Jared Proffitt',
    url='https://github.com/fabric-bolt/fabric-bolt',
    description='A web interface to fabric deployments.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['docs', ]),
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
        'Programming Language :: Python',
    ],
)
