from setuptools import setup
import os

version = "1.0.2"
current = os.path.abspath(os.path.dirname(__file__))
# Getting long description
with open(os.path.join(current, "README.md"), "r") as f:
    readme = f.read()

setup(
    name="quickrepo",
    version=version,
    url="https://www.github.com/silverhairs/quickrepo",
    author="Boris Kayi",
    author_email="boriskayienzo@gmail.com",
    description="Command-line tool to automate git and github repository creation.",
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms="any",
    python_requires=">=3.6",
    packages=["quickrepo"],
    py_modules=["quickrepo"],
    install_requires=["Click", "PyGithub", "gitpython", "colorama",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
    [console_scripts]
    quickrepo=quickrepo:cli
    """,
)
