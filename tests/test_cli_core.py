import os
import click
from pytijo_cli.cli import tijo
import json
from click.testing import CliRunner


def get_test_file(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def read(filename):
    with open(get_test_file(filename), "r") as fin:
        return fin.read()


# TODO remove this test
def test_mockup():
    pass


# TODO do following test
"""
def test_basic_command():
    runner = CliRunner()
    result = runner.invoke(
        tijo,
        [
            "tijo",
            "cat",
            "%s" % get_test_file("cli.output.1"),
            "--tijo-template",
            "%s" % get_test_file("cli.template.1"),
            "--tijo-output-beauty",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.output) == json.loads(read("cli.parsed.1"))
"""
