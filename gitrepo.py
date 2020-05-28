import click
import os
import sys
import subprocess
import git
from github import Github


# Create repository on github and clone it locally
def create_and_clone_repo(user, repo_name, private, desc):
    try:
        click.echo(f'Creating repository {repo_name} ...')

        user.create_repo(  
            name=repo_name,
            description=desc,
            private=not private,
            auto_init=True,
        )
        repo_url = user.get_repo(repo_name).clone_url
        # Clone repo in the working directory
        git.Git(os.getcwd()).clone(repo_url)
        click.secho('Repository successfully created! 🔥️🔥️', fg='green')
    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')


# Initialize a repo from current directory and push it on github
def repo_from_cwd(cwd, cwd_tree, user):
    is_private = click.prompt('Should the repository be private?\n[y/N]: ')
    private = True if is_private.lower() == 'y' else False
    desc = click.prompt('Description: ', default='')

    try:
        user.create_repo(name=cwd, description=desc, private=private)
        url = user.get_repo(cwd).clone_url
    except Exception as e:
        print(f'{repr(e)}')
        sys.exit()

    repo = git.Repo.init(path=cwd_tree)
    git.Remote.add(repo, name='origin', url=url)
    # If repo doesn't have a .gitignore request one (not mandatory)
    if not os.path.exists('.gitignore'):
        gitignore_status = click.prompt('No .gitignore file detected, add anyway ? [y/N]: ')
        if gitignore_status.lower() == 'y':
            subprocess.run(['git', 'add', '.'])
            commit_msg = click.prompt('Commit message: ', default='Initial commit')
            subprocess.run(['git', 'commit', '-m', commit_msg])
            try:
                subprocess.run(['git', 'push', 'origin', 'master'])
            except Exception as e:
                print(f'{repr(e)}')
                sys.exit()
        else:
            sys.exit()
    click.secho(f'Initiazed repo {cwd} locally and on github.com', fg='green')
    

# Main function
@click.command()
@click.argument('here', required=False)
def main(here):
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    connection = Github(username, password)
    try:
        user = connection.get_user()
    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')
        sys.exit()

    click.secho('User authenticated', fg='blue')
    CURRENT_DIR_NAME = os.path.basename(os.getcwd())
    '''If user adds argument "here" then init local and github repo from current directory
     Otherwise, generate a new repository on github and clone it at the current directory'''
    if here:
        repo_from_cwd(cwd=CURRENT_DIR_NAME, cwd_tree=os.getcwd, user=connection.get_user())
    else:
        repo_name = click.prompt('Repo name: ')
        private = click.prompt('Should the repository be private?\n[y/N]: ')
        count = 1
        while count > 0:
            if private.lower() == 'y' or private.lower() == 'yes':
                private = True
                count -=1
            elif private.lower() == 'n' or private.lower() == 'no':
                private = False
                count-=1
            else:
                click.echo('Invalid input!')
                private = click.prompt('Should the repository be private?\n[y/N]: ')

        desc = click.prompt('Description: ', default='')
        create_and_clone_repo(user=connection.get_user(), repo_name=repo_name, private=private, desc=desc)

