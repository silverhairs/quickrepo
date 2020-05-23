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
        is_public = True

    try:
        user.get_user().create_repo(  # Creating a repository on github
            name=name,
            private=not is_public,
            auto_init=True,
        )

        repo_url = user.get_user().get_repo(name).clone_url
        print(f'Repository created on github, here is the url: {repo_url}')

    except BadCredentialsException:
        print('Wrong username or password')