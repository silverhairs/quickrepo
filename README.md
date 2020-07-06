# quickrepo
![fury](https://badge.fury.io/py/quickrepo.svg)
![pipy](https://pypip.in/d/quickrepo/badge.png)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

It is quite boring everytime typing `git init` in your local computer then go to github and initialize a new repository, take the remote url and add it to the local... I am already tired just by explaining. Thanks God **quickrepo** exists. <br/>
<br/>quickrepo is a command-line application that automates initializing a new repository both locally and on GitHub. The user can either initialize the repository in the directory they are currently working in, or generate a brand new folder which will come initialized as a git and github repository.

<img src="/demo.gif" alt="demo">

## Requirements
- Python 3.6^
## Installation
<b>install the official package from PyPI</b>
```
pip install quickrepo
```
If you have multiple versions of Python installed in your system, use `pip3 install quickrepo` instead.

<b>or install editable source code</b>
```
git clone github.com/silverhairs/quickrepo.git
cd quickrepo
pip install --editable .
```

## Usage
Run `quickrepo` to list all the available commands.

#### Initialize a new Git & Github repository
To generate a brand new project both locally and on Github, open your terminal/command prompt and run: </br>
```
quickrepo new
```
#### Initialize current working directory as Git & Github repository
To initialize a Git repository in the current working directory and push the content on Github, open your terminal/command prompt and run </br>
```
quickrepo here
```

