# coding: utf-8

from setuptools import setup, find_packages

setup(
    name             = 'googlefinance.get',
    version          = '0.4.2',
    packages         = find_packages(),   # ['googlefinance.get'],  # same as the name above
    description      = 'googlefinance.get is a single function from google finance api to DataFrame.',
    license          = 'MIT',
    author           = 'Yong Beom Kim',
    author_email     = 'saltman21@naver.com',
    url              = 'https://github.com/YongBeomKim/googlefinance.get',
    download_url     = 'https://github.com/YongBeomKim/googlefinance.get/dist/googlefinance.get-0.4.2-py3-none-any.whl',
    keywords         = 'googlefinance',
    install_requires = ['requests', 'pandas'],
    classifiers      = ['Programming Language :: Python :: 3.6',
                        'Intended Audience :: Financial and Insurance Industry',
                        'License :: OSI Approved :: MIT License']
    )