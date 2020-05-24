import click
import os
import git
from github import Github, GithubException


@click.command()
def start():
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    connection = Github(username, password)
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

    except GithubException.BadCredentialsException as error:
        click.echo(
            click.style(str(error['message']).capitalize() + ' ❌❌', fg='red'))
