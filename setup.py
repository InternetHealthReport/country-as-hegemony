# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='country-as-hegemony',
    version='0.1.1',
    description="Measuring AS dependency of a country",
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Romain Fontugne',
    url='https://github.com/InternetHealthReport/country-as-hegemony',
    packages=find_packages(exclude=('tests', 'docs')),
    scripts=['bin/country-hege'],
    install_requires=[
        'abondance',
        'arrow',
        'iso3166',
        ]
)

