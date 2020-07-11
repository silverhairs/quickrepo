from setuptools import setup
import os

current = os.path.abspath(os.path.dirname(__file__))
# Getting long description
with open(os.path.join(current, "README.md"), "r") as f:
    readme = f.read()

setup(
    name="quickrepo",
    version="1.0.4",
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
    install_requires=[
        "click==7.1.2",
        "click-spinner==0.1.10",
        "PyGithub==1.51",
        "GitPython==3.1.3",
        "colorama==0.4.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={"test": ["pytest==5.4.3",]},
    entry_points="""
    [console_scripts]
    quickrepo=quickrepo:main
    """,
)
