#!/usr/bin/env  python3
import click
import os
import sys
import git
from github import Github

BOLD_TEXT = "\033[1m"

@click.group()
@click.version_option(version="1.0.1")
def cli():
    """
    A CLI tool to initialize a repository both locally and on GitHub
    """

# generate new repository folder
@cli.command()
def new():
    """
    Generate a new Github repository folder in the current location
    """
    credentials = input_credentials()
    repo_name = click.prompt("Repository name: ")
    
    try:
        click.secho(f"{BOLD_TEXT}Creating repository {repo_name} ...", fg="blue")
        credentials['user'].create_repo(
            name=repo_name,
            description=credentials["desc"],
            private=credentials["is_private"],
            auto_init=True,
        )
        # Clone repo in current directory
        url = credentials['user'].get_repo(repo_name).clone_url
        git.Git(os.getcwd()).clone(url)
        click.secho(f"{BOLD_TEXT}Repository successfully created! 🔥️🔥️", fg="green")
    except Exception as e:
        click.secho(f"{repr(e)}", fg="red")


# Initialize git and github on current folder
@cli.command()
def here():
    """
    Initialize the current directory as a git and github repository
    """
    credentials = input_credentials()
    cwd = os.getcwd()  # current working directory
    cwf = os.path.basename(cwd)  # current working folder

    # Check if there is a .gitignore file
    if not os.path.exists(".gitignore"):
        click.secho(f"{BOLD_TEXT}No .gitignore detected, continue anyway?")
        gitignore_status = click.prompt(
            "1- Yeah, Let's continue\n2- No, stop everything, I must create it first\n"
        )
        count = 1
        while count > 0:
            if gitignore_status == "2":
                count -= 1
                sys.exit("Aborted!")
            elif gitignore_status == "1":
                count -= 1
            else:
                click.echo(f"{BOLD_TEXT}Invalid input!")
                gitignore_status = click.prompt(
                    "1- Yes, it's no big deal\n2- No, I must create it first\n"
                )
    try:
        click.secho(f"{BOLD_TEXT}Initializing repository...", fg="blue")
        credentials['user'].create_repo(
            name=cwf, description=credentials["desc"], private=credentials["is_private"]
        )
        url = credentials['user'].get_repo(cwf).clone_url
    except Exception as e:
        click.secho(f"{BOLD_TEXT}{repr(e)}", fg="red")
        sys.exit("Aborted!")

    repo = git.Repo.init(path=cwd)
    remote = repo.create_remote(name="origin", url=url)
    # Add and commit files
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    for f in files:
        repo.index.add([f"{cwd}/{f}"])
    commit_msg = click.prompt("Commit message ", default="Initial commit")
    repo.index.commit(message=commit_msg)
    # Push to github.com in master branch
    try:
        remote.push(refspec="master:master")
        click.secho(f"{BOLD_TEXT}Initiazed {cwf} locally and on github.com 🔥️🔥️", fg="green")
    except Exception as e:
        click.secho(f"{repr(e)}", fg="red")
        sys.exit("Aborted!")


# User enters his credentials
def input_credentials():

    username = click.prompt("Username for github.com")
    pw = click.prompt("Password for github.com", hide_input=True)
    user = Github(username, pw).get_user()

    private = click.prompt("Should the repository be private? [y/N] ")
    count = 1
    while count > 0:
        if private.lower() == "y" or private.lower() == "yes":
            private = True
            count -= 1
        elif private.lower() == "n" or private.lower() == "no":
            private = False
            count -= 1
        else:
            click.echo(f"{BOLD_TEXT}Invalid input!")
            private = click.prompt("Should the repository be private? [y/N] ")
    desc = click.prompt("Description ", default="")

    return {
        "user": user,
        "is_private": private,
        "desc": desc,
    }
