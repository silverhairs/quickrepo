import click
import os
import sys
import git
from github import Github


# This function generates a txt file that holds the username
def generate_username_file(file_name, username):
    # Hide file in (Unix systems)
    prefix = '.' if os.name != 'nt' else ''
    file_name = f'{prefix}{file_name}'
    # Write username inside file
    with open(file_name, 'w') as f:  # Create  file
        f.write(f'{username}')
        f.close()


# Create repository on github.com and clone it locally
def create_and_clone_repo(user):
    repo_name = click.prompt('Repo name: ')
    public = click.prompt('Should the repository be public?\n[y/N]: ')

    count = 1
    while count > 0:
        if public.lower() == 'y' or public.lower() == 'yes':
            public = True
            count -=1
        elif public.lower() == 'n' or public.lower() == 'no':
            public = False
            count-=1
        else:
            click.echo('Invalid input!')
            public = click.prompt('Should the repository be public?\n[y/N]: ')
    
    desc = click.prompt('Description: ')


    try:
        click.echo(f'Creating repository {repo_name} ...')

        user.create_repo(  
            name=repo_name,
            description=desc,
            private=not public,
            auto_init=True,
        )
        repo_url = user.get_repo(repo_name).clone_url

        git.Git(os.getcwd()).clone(repo_url)
        click.secho('Repository successfully created! 🔥️🔥️', fg='green')

    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')


@click.command()
def main():
    connection = None

    # If the username file exists, use it, else requests credentials and generate the file
    if os.path.exists('.username_holder.txt'):
        password = click.prompt('Enter GitHub password: ', hide_input=True)
        with open('.username_holder.txt') as f:
            for line in f:
                username = line
            connection = Github(username, password)
            f.close()

    else:
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        connection = Github(username, password)
    try:
        user = connection.get_user() #FIXME: request not being made
        click.secho('User authenticated\n', fg='green')
    except Exception as e:
        click.secho(f'{repr(e)}', fg='red')
        sys.exit()

    generate_username_file('username_holder.txt', username)
    create_and_clone_repo(user)