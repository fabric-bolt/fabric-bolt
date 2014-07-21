#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'django>=1.6.5,<1.7',
    'south>=0.8.4,<0.9',
    'pillow>=2.5.1,<2.6',
    'django-stronghold>=0.2.6,<0.3',
    'django-crispy-forms>=1.4.0,<1.5',
    'django-custom-user>=0.4,<0.5',
    'django-tables2>=0.15.0,<0.16',
    'django-braces>=1.4,<1.5',
    'django-sekizai>=0.7,<0.8',
    'django-grappelli>=2.5.1,<2.6',
    'fabric>=1.9,<1.10',
    'logan>=0.5.10,<0.6',
    'GitPython>=0.3.1,<0.4',
    'django-bootstrap-form>=3.1,<3.2',
    'croniter==0.3.4',
    'gevent-socketio>=0.3.6,<0.4',
]

dev_requires = [
    'django_debug_toolbar>=1.2.1,<1.3',
    'django-grappelli>=2.5.3,<2.6',
    'django-debug-toolbar-template-timings>=0.6.4,<0.7',
    'mock>=1.0.1,<1.1',
]

postgres_requires = [
    'psycopg2>=2.5.3,<2.6',
]

mysql_requires = [
    'MySQL-python>=1.2.5,<1.3',
]


setup(
    name='fabric-bolt',
    version='0.1b1',
    author='Dan Dietz, Nathaniel Pardington, Jared Proffitt',
    url='https://github.com/worthwhile/fabric-bolt',
    description='A web interface to fabric deployments.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['docs',]),
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