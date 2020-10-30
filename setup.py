from setuptools import setup, find_packages

from os.path import join, dirname
import sys
sys.path.insert(0, join(dirname(__file__), 'lib'))
sys.path.pop(0)

setup(
    name="PyRindow-CMS-Pages",
    version="0.2.0",
    description="Web Page Generator",
    author="Rindow",
    url="https://github.com/rindow/pyrindow-framework",
    author_email="rindow dot io",
    license="BSD 3-Clause",    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords="web pages template",
    packages=find_packages('lib'),
    namespaces=['pyrindow.cms.pages'],
    package_dir={'': 'lib'},
)
