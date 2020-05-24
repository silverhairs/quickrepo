import click
import os
import git
from github import Github
from github.GithubException import BadCredentialsException


@click.command()
def start():
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    user = Github(username, password)
    name = click.prompt('Repo name: ')
    is_public = click.prompt('Should the repository be public? (y/N)\n')

    if is_public.lower() == 'y' or is_public.lower() == 'yes':
        is_public = True
    elif is_public.lower() == 'n' or is_public.lower() == 'no':
        is_public = False
    else:
        is_public = True  #FIXME: abort the program when user inputs a wrong key

    try:
        user.get_user().create_repo(  # Creating a repository on github
            name=name,
            private=not is_public,
            auto_init=True,
        )

        repo_url = user.get_user().get_repo(name).clone_url

        git.Git(os.path.dirname(os.path.realpath(__file__))).clone(repo_url) # Clone the repo locally
        click.echo('🔥️🔥️ Repository successfully created!')

    except BadCredentialsException:
        click.echo('Wrong username or password')


#TODO:
"""
PS: Next time you pull the project, please reinstall it before doing anything (pip install --editable .)

Next Tasks
- Login to Github ✔️
- Create repo on github ✔️
- Clone repo locally ✔️
- Set a right path where the directory should be
- Setup login with SSH
- Write tests
- Output a program description and version
"""