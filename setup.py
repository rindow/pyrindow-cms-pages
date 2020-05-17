from setuptools import setup, find_packages

from os.path import join, dirname
import sys
sys.path.insert(0, join(dirname(__file__), 'lib'))
from pyrindow import __version__
sys.path.pop(0)

setup(
    name="PyRindow-Framework",
    version=__version__,
    description="IoC container based Application Framework",
    author="Rindow",
    url="https://github.com/rindow/pyrindow-framework",
    author_email="rindow dot io",
    license="BSD 3-Clause",    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords="ioc container framework",
    packages=find_packages('lib'),
    namespaces=['pyrindow'],
    package_dir={'': 'lib'},
)
