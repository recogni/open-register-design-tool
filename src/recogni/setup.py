from setuptools import setup
from setuptools import find_packages

packages = find_packages()
packages.append("system_rdl")

setup(name="system_rdl",
      version="0.0.1",
      description="Recogni SystemRDL grammar parser",
      url="https://github.com/recogni/open-register-design-tool",
      author="recogni",
      install_requires=[
      ],
      packages=packages)
