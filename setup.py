from setuptools import setup

setup(
    name='Git-Repo',
    version='1.0',
    author='Boris Kayi & Herve Musangwa',
    description='A CLI app to create a new git repository both locally and remotely',
    install_requires=[
        'Click',
        'PyGithub'
    ],
    entry_points='''
    [console_scripts]
    gitrepo=gitrepo:create
    '''
)