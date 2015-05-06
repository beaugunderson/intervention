from setuptools import find_packages, setup

setup(
    name='intervention',
    author='Beau Gunderson',
    author_email='beau@beaugunderson.com',

    url='https://github.com/beaugunderson/intervention',

    description='An intervention to increase intentionality',
    long_description_markdown_filename='README.md',

    keywords=['adhd', 'anxiety', 'intervention', 'quantified self'],

    version='1.0.0',

    license='MIT',

    packages=find_packages(),

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'intervention = intervention.launch:main',
        ]
    },

    install_requires=[
        'arrow==0.5.4',
        'pyobjc-core==3.0.4',
        'pyobjc==3.0.4',
        'PySide==1.2.2',
        'tini>=3.0.1',
    ],

    setup_requires=[
        'setuptools-markdown'
    ],

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
