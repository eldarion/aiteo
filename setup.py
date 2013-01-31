from setuptools import setup, find_packages


setup(
    name = "aiteo",
    version = "1.0b1.dev1",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "aiteo is an app for asking questions",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/aiteo",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)