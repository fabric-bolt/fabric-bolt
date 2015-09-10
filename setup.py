#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'django==1.8.4',
    'pillow==2.9.0',
    'django-stronghold==0.2.7',
    'django-crispy-forms==1.5.1',
    'django-authtools==1.2.0',
    'django-tables2==1.0.4',
    'django-braces==1.8.1',
    'django-sekizai==0.8.2',
    'fabric==1.10.2',
    'logan==0.7.1',
    'django-bootstrap-form==3.2',
    'croniter==0.3.8',
    'GitPython==1.0.1',
    'gevent-socketio==0.3.6',
    'django-graphos==0.0.2a0',
    'django-activeurl==0.1.8',
    'requests==2.7.0',
    'virtualenv==13.1.0',
    'django-grappelli==2.7.1',
]

dev_requires = [
    'django-debug-toolbar==1.3.2',
    'django-debug-toolbar-template-timings==0.6.4',
    'mock==1.3.0',
    'model_mommy==1.2.5'
]

postgres_requires = [
    'psycopg2==2.6.1',
]

mysql_requires = [
    'MySQL-python==1.2.5',
]


setup(
    name='fabric-bolt',
    version='0.1',
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
