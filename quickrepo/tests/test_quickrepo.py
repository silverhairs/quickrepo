import pytest
from click.testing import CliRunner
import quickrepo


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_quickrepo(runner):
    result = runner.invoke(quickrepo.main)
    assert result.exit_code == 0
    assert (
        "A CLI tool to initialize a repository both locally and on GitHub"
        in result.output
    )

