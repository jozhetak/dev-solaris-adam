from setuptools import find_packages, setup

from adam.version import __version__, licence
from adam import __doc__, __author__, __author_email__

setup(
    name="tangods-adam",
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    license=licence,
    description="A sample Python project",
    long_description=__doc__,
    url="https://github.com/synchrotron-solaris/dev-solaris-adam.git",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["setuptools"],
    entry_points={
        "console_scripts": ["ADAM = "
                            "adam.run_server:main"]}
)
