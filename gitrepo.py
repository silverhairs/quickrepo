#!/usr/bin/env  python3

import click
import os
import sys
import git
from github import Github

BOLD_TEXT='\033[1m'

# Initialize git and github repo in new directory and generate it
def init_new_dir(user, repo_name, private, desc):
    try:
        click.secho(f'{BOLD_TEXT}Creating repository {repo_name} ...', fg='blue')
        user.create_repo(  
            name=repo_name,
            description=desc,
            private=not private,
            auto_init=True,
        )
        # Clone repo in current directory
        repo_url = user.get_repo(repo_name).clone_url
        git.Git(os.getcwd()).clone(repo_url)
        click.secho(f'{BOLD_TEXT}Repository successfully created! 🔥️🔥️', fg='green')
    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')


# Initialize a git and github repo in the current directory
def init_cwd(cwd, cwd_path, user, private, desc):
    # If repo doesn't have a .gitignore, remind user to create one (Not mandatory though)
    if not os.path.exists('.gitignore'):
        click.secho(f'{BOLD_TEXT}No .gitignore detected, continue anyway?')
        gitignore_status = click.prompt("1- Yeah, Let's continue\n2- OMG! stop everything, I must create it first\n")
        count = 1
        while count > 0:
            if gitignore_status == '2':
                count-=1
                sys.exit('Aborted')
            elif gitignore_status == '1':
                count-=1
            else:
                click.echo(f'{BOLD_TEXT}Oops... wrong input!')
                gitignore_status = click.prompt("1- Yeah, I don't care\n2- OMG! stop everything, I must create it first\n")
    try:
        click.secho(f'{BOLD_TEXT}Getting url...', fg='cyan')
        user.create_repo(name=cwd, description=desc, private=private)
        url = user.get_repo(cwd).clone_url
    except Exception as e:
        print(f'{repr(e)}')
        sys.exit('Aborted!')

    repo = git.Repo.init(path=cwd_path)
    remote = repo.create_remote(name='origin', url=url)
    remote.fetch()
    # Add and commit files to local repo
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        repo.index.add([f'{cwd_path}/{file}'])
    commit_msg = click.prompt('Commit message ', default='Initial commit')
    repo.index.commit(message=commit_msg)
    try:
        remote.push(refspec='master:master') #FIXME: We shouldn't receive another request of credentials
        click.secho(f'Initiazed repo {cwd} locally and on github.com', fg='green')
    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')
        sys.exit('Aborted!')


# Main function
@click.command()
@click.argument('here', required=False)
def main(here):
    '''
    Initialize a repository in both GitHub and your local computer with a single command.
    '''
    if here:
        if here != 'here':
            sys.exit(f'{BOLD_TEXT}Unknown argument {here}')

    username = click.prompt('Username for github.com')
    password = click.prompt('Password for github.com', hide_input=True)
    connection = Github(username, password)
    try:
        user = connection.get_user()
    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')
        sys.exit('Aborted!')

    private = click.prompt('Should the repository be private? [y/N] ')
    count = 1
    while count > 0:
        if private.lower() == 'y' or private.lower() == 'yes':
            private = True
            count -=1
        elif private.lower() == 'n' or private.lower() == 'no':
            private = False
            count-=1
        else:
            click.echo(f'{BOLD_TEXT}Invalid input!')
            private = click.prompt('Should the repository be private? [y/N] ')
    desc = click.prompt('Description ', default='')

    current_dir = os.path.basename(os.getcwd())

    '''If user adds argument "here" then init local and github repo from current directory
     Otherwise, generate a new repository on github and clone it at the current directory'''
    if here:
        init_cwd(cwd=current_dir.replace(' ', ''), cwd_path=os.getcwd(), user=connection.get_user(), private=private, desc=desc)
    else:
        repo_name = click.prompt('Repo name: ')
        init_new_dir(user=connection.get_user(), repo_name=repo_name, private=private, desc=desc)