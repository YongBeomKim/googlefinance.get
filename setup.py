# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")


setup(
    name             = 'googlefinance.get',
    version          = '0.4.1',
    packages         = find_packages(),
    # packages         = ['googlefinance.get'], # this must be the same as the name above
    description      = 'googlefinance.get is a single function from google finance api to DataFrame.',
    license          = 'MIT',
    author           = 'erdos',
    author_email     = 'saltman21@naver.com',
    url              = 'https://github.com/YongBeomKim/googlefinance.get/blob/master/dist/googlefinance.get-0.4.1-py3-none-any.whl',
    keywords         = 'googlefinance',
    install_requires = ['requests', 'pandas'],
    classifiers      = ['Programming Language :: Python :: 3.6',
                        'Intended Audience :: Financial and Insurance Industry',
                        'License :: OSI Approved :: MIT License']
    )