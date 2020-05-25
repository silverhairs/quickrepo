import click
import os
import git
from github import Github, GithubException, Badusername_holderException, BadCredentialsException


# This function generates a txt file that holds username
def generate_username_file(file_name, username):
    # Hide file in (Unix systems)
    prefix = '.' if os.name != 'nt' else ''
    file_name = f'{prefix}{file_name}'

    # Write username inside file
    with open(file_name, 'w') as f:  # Create  file
        f.write(f'{username}')
        f.close()
    # File Key



@click.command()
def start():
    connection = None

    # If file exists, fetch username and connect, else request all the username_holder and generate file
    if os.path.exists('.username_holder.txt'):
        password = click.prompt('Enter GitHub password: ', hide_input=True)
        with open('.username_holder.txt') as f:
            cred = {}
            for line in f:
                username = line
            connection = Github(username, password)
            f.close()

    else:
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        connection = Github(username, password)

        generate_username_file('username_holder.txt', username)

    name = click.prompt('Repo name: ')
    is_public = click.prompt('Should the repository be public?\n[y/N]: ')
    
    # If user enter y or yes, repo is public, user enters n or no, repo is private else, reask question until users gives valid answer
    count = 1
    while count > 0:
        if is_public.lower() == 'y' or is_public.lower() == 'yes':
            is_public = True
            count -=1
        elif is_public.lower() == 'n' or is_public.lower() == 'no':
            is_public = False
            count-=1
        else:
            click.echo('Invalid input!')
            is_public = click.prompt('Should the repository be public?\n[y/N]: ')


    try:
        # Create a repo on github
        connection.get_user().create_repo(  
            name=name,
            private=not is_public,
            auto_init=True,
        )
        # Clone the repo locally
        repo_url = connection.get_user().get_repo(name).clone_url
        git.Git(os.getcwd()).clone(repo_url)

        click.echo(click.style('Repository successfully created! 🔥️🔥️', fg='green'))

    except GithubException as error:
        click.echo(
            click.style(str(error.data['errors'][0]['message']).capitalize(),
                        fg='red'))

    except Badusername_holderException as error:
        click.echo(
            click.style(str(error['message']).capitalize() + ' ❌❌', fg='red'))
        
    except BadCredentialsException:
        click.echo(click.style('Wrong username or password'), fg='red')