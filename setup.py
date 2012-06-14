#!/usr/bin/env python

try:
	from setuptools import setup, find_packages
except ImportError:
	from ez_setup import use_setuptools
	use_setuptools()
	from setuptools import setup, find_packages

setup(
    name='django-featured-item',
    version="0.1.0",
    description='Mark a single record in a model as featured',
    author='Tim Heap',
    author_email='heap.tim@gmail.com',
    url='https://bitbucket.org/tim_heap/django-featured-item',
    packages=['featured_item',],
    install_requires = ['Django>=1.4'],
    package_data={},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

