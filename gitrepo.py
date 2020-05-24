import click
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

        repo_url = user.get_user().get_repo(name).clone_url  # Getting url of created repo
        click.echo(f'Repository created on github, here is the url: {repo_url}')

    except BadCredentialsException:
        print('Wrong username or password')

#TODO:
"""
Next time you pull the project, please reinstall the package (pip install --editable .) first.

TODO: Next Tasks
- Run git command with python script: git clone especially
- Setup login with SSH
"""