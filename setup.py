from distutils.core import setup



setup(
    name = "aiteo",
    version = "0.1.dev1",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "aiteo is an app for asking questions",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/agora",
    packages = [
        "aiteo",
        "aiteo.templatetags",
    ],
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