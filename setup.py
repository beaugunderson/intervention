#!/usr/bin/env python

import sys

from setuptools import find_packages, setup

install_requires = [
    'arrow==0.5.4',
    'PySide==1.2.2',
    'tini>=3.0.1',
]

if sys.platform == 'darwin':
    # PyObjc is only required on OS X
    install_requires.extend([
        'pyobjc-core==3.0.4',
        'pyobjc==3.0.4',
    ])
elif sys.platform.startswith('win'):
    # pywin32 is only required on Windows
    install_requires.extend([
        'pypiwin32==219',
    ])

setup_requires = []

# I only release from OS X so markdown/pypandoc isn't needed in Windows
if not sys.platform.startswith('win'):
    setup_requires.extend([
        'setuptools-markdown',
    ])

setup(
    name='intervention',
    author='Beau Gunderson',
    author_email='beau@beaugunderson.com',

    url='https://github.com/beaugunderson/intervention',

    description='An intervention to increase intentionality',
    long_description_markdown_filename='README.md',

    keywords=['adhd', 'anxiety', 'intervention', 'quantified self'],

    version='1.1.0',

    license='MIT',

    packages=find_packages(),

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'intervention = intervention.launch:main',
        ]
    },

    install_requires=install_requires,

    setup_requires=setup_requires,

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',

        'Topic :: Utilities',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ])
