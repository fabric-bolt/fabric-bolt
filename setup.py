#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'django>=1.8.3,<1.9',
    'pillow>=2.9.0,<2.10',
    'django-stronghold>=0.2.7,<0.3',
    'django-crispy-forms>=1.4.0,<1.5',
    'django-authtools>=1.2.0,<1.3',
    'django-tables2>=1.0.4,<1.1',
    'django-braces>=1.8.1,<1.9',
    'django-sekizai>=0.8.2,<0.9',
    'fabric>=1.10.2,<1.11',
    'logan>=0.7.1,<0.8',
    'django-bootstrap-form>=3.2,<3.3',
    'croniter>=0.3.8,<0.4',
    'GitPython>=1.0.1,<1.1',
    'gevent-socketio>=0.3.6,<0.4',
    'django-graphos==0.0.2a0',
    'django-activeurl>=0.1.8,<0.2',
    'requests>=2.7.0,<2.8',
    'virtualenv>=13.1.0,<13.2',
    'django-grappelli>=2.7.1,<2.8',
]

dev_requires = [
    'django-debug-toolbar>=1.3.2,<1.4',
    'django-debug-toolbar-template-timings>=0.6.4,<0.7',
    'mock>=1.3.0,<1.4',
    'model_mommy>=1.2.5,<1.3'
]

postgres_requires = [
    'psycopg2>=2.6.1,<2.7',
]

mysql_requires = [
    'MySQL-python>=1.2.5,<1.3',
]


setup(
    name='fabric-bolt',
    version='0.1b1',
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
        'Programming Language :: Python'
    ],
)
