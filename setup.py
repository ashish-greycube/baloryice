# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in baloryice/__init__.py
from baloryice import __version__ as version

setup(
	name='baloryice',
	version=version,
	description='Sales customizations',
	author='greycube.in',
	author_email='info@greycube.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
