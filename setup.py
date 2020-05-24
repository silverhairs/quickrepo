from setuptools import setup

version='1.0'
setup(
    name='Git-Repo',
    version=version,
    author='Boris Kayi & Herve Musangwa',
    description='A CLI app to create a new git repository both locally and remotely',
    install_requires=[
        'Click',
        'PyGithub',
        'gitpython',
        'colorama',
    ],
    entry_points='''
    [console_scripts]
    gitrepo=gitrepo:start
    '''
)