import os
from setuptools import setup


def read(file_name):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="pytube",
    version="0.6",
    author="Richard Hayes",
    author_email="rich@justcompile.it",
    install_requires=required,
    description="Youtube API V3 feed parser",
    license="BSD",
    keywords="youtube api",
    url="http://packages.python.org/pytube",
    packages=['pytube'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
