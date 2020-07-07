import pytest
from unittest import mock
from click.testing import CliRunner
import quickrepo


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_quickrepo(runner):
    result = runner.invoke(quickrepo.main)
    assert not result.exception
    assert (
        "A CLI tool to initialize a repository both locally and on GitHub"
        in result.output
    )


def test_command_new(runner):
    result = runner.invoke(
        quickrepo.new, ["-u", "john-doe", "-p", "password", "-n", "test"]
    )
    assert not result.exception
    assert "Bad credentials" in result.output


def test_command_here(runner):
    result = runner.invoke(
        quickrepo.here, ["-u", "not-john", "-p", "not-my-password"], input="y"
    )

    assert "no gitignore" in result.output
    assert result.exit_code == 0

