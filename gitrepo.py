import click
import os
import subprocess
import git
from github import Github, GithubException, BadCredentialsException


# This function generates a txt file that holds user credentials
def generate_credentials_hidden_file(file_name, username, pw):  #FIXME: this function is not secured enough we should add some encryption
    prefix = '.' if os.name != 'nt' else '' #  For Unix systems
    
    file_name = subprocess.check_call(["attrib", "+H", file_name]) if os.name == 'nt' else f'{prefix}{file_name}'

    with open(file_name, 'w') as f:  # Create hidden file
        f.write(f'username:{username}\npassword:{pw}')
        f.close()


@click.command()
def start():
    username = None
    password = None
    connection = None

    # Check if the credentials file was generated
    if os.path.exists('.credentials.txt'):
        with open('.credentials.txt') as f:
            cred = {}
            for line in f:
                label, value = line.split(':')
                cred[label] = str(value)

            connection = Github(cred['username'].replace("\n", ''),
                                cred['password'])  # Connect from file
    else:
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        connection = Github(username, password)

        generate_credentials_hidden_file('credentials.txt', username,
                                  password)  # Generate file

    name = click.prompt('Repo name: ')
    is_public = click.prompt('Should the repository be public? (y/N)\n')

    if is_public.lower() == 'y' or is_public.lower() == 'yes':
        is_public = True
    elif is_public.lower() == 'n' or is_public.lower() == 'no':
        is_public = False
    else:
        is_public = True  #FIXME: abort the program when user enters a wrong key

    try:
        connection.get_user().create_repo(  # Creating a repo on github
            name=name,
            private=not is_public,
            auto_init=True,
        )

        repo_url = connection.get_user().get_repo(
            name).clone_url  # Getting URL of the created repo

        git.Git(os.path.dirname(os.path.realpath(__file__))).clone(
            repo_url)  # Clone the repo locally
        click.echo(
            click.style('Repository successfully created! 🔥️🔥️', fg='green'))

    except GithubException as error:
        click.echo(
            click.style(str(error.data['errors'][0]['message']).capitalize(),
                        fg='red'))

    except BadCredentialsException as error:
        click.echo(
            click.style(str(error['message']).capitalize() + ' ❌❌', fg='red'))
