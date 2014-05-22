import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pytube",
    version = "0.0.1",
    author = "Richard Hayes",
    author_email = "rich@justcompile.it",
    description = ("Youtube API V2 feed parser"),
    license = "BSD",
    keywords = "youtube api",
    url = "http://packages.python.org/pytube",
    packages=['pytube'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)