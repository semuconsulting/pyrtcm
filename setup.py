"""
Created on 14 Feb 2022

@author: semuadmin
"""
import setuptools

from pyrtcm import version as VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrtcm",
    version=VERSION,
    author="semuadmin",
    author_email="semuadmin@semuconsulting.com",
    description="RTCM3 Protocol Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/semuconsulting/pyrtcm",
    packages=setuptools.find_packages(
        exclude=["tests", "examples", "references", "docs"]
    ),
    license="BSD 3-Clause 'Modified' License",
    keywords="PYRTCM GNSS GPS RTCM RTCM3 GIS NTRIP",
    platforms="Windows, MacOS, Linux",
    project_urls={
        "Bug Tracker": "https://github.com/semuconsulting/pyrtcm",
        "Documentation": "https://github.com/semuconsulting/pyrtcm",
        "Sphinx API Documentation": "https://www.semuconsulting.com/pyrtcm",
        "Source Code": "https://github.com/semuconsulting/pyrtcm",
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: BSD License",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.7",
)
