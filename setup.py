from setuptools import find_namespace_packages, setup

def get_requirements():
    pass

setup(
    name="sensor",
    version="0.0.1",
    author="ineuron",
    author_email="amardeepkumar6007@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements(), #["pymongo==4.2.0"],
    )
