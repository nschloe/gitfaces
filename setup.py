# -*- coding: utf-8 -*-
#
from distutils.core import setup
import os
import codecs

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, 'gitfaces', '__about__.py')) as f:
    exec(f.read(), about)


def read(fname):
    try:
        content = codecs.open(
            os.path.join(os.path.dirname(__file__), fname),
            encoding='utf-8'
            ).read()
    except Exception:
        content = ''
    return content


setup(
    name='gitfaces',
    version=about['__version__'],
    packages=['gitfaces'],
    url='https://github.com/nschloe/gitfaces',
    download_url='https://pypi.python.org/pypi/gitfaces',
    author=about['__author__'],
    author_email=about['__email__'],
    install_requires=[
        'GitPython',
        'Pillow',
        'pipdated',
        'requests',
        ],
    description='fetch contributor avatars for a GitHub repository',
    long_description=read('README.rst'),
    license=about['__license__'],
    classifiers=[
        about['__status__'],
        about['__license__'],
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Version Control',
        ],
    scripts=[
        'tools/gitfaces'
        ]
    )
