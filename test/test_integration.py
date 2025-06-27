"""
Implementation of the integration tests for the library.
"""

import functools
import shlex
import subprocess

from dataclasses import dataclass
from importlib import metadata
from typing import Any, Callable

import pytest


LIST_COMMAND_FMT = "list --group-name {group_name}"
EXEC_COMMAND_FMT = (
    "exec --group-name {group_name} --entry-point {entry_point} {raw_data}"
)


@dataclass
class EntryPointOutput:
    stdout: str
    stderr: str
    result: bytes


def requires_installed_package(package_name) -> Callable:
    """
    A decorator for skipping a test if the given package isn't installed.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            _ = pytest.importorskip(package_name)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@pytest.fixture
def entry_point_output(request, capsys) -> EntryPointOutput:
    """
    Capture the output of a given entry point (the arguments are taken from request.param)
    """
    group_name, entry_point_name, data = request.param
    entry_points: metadata.EntryPoints = metadata.entry_points()
    group_entries = entry_points.select(group=group_name)
    entry_point = [ep.load() for ep in group_entries if ep.name == entry_point_name][0]

    result = entry_point(data)
    captured = capsys.readouterr()

    return EntryPointOutput(captured.out, captured.err, result)


@pytest.mark.parametrize(
    "cmd",
    [
        " ".join(
            [
                "--no-interpreter-init",
                LIST_COMMAND_FMT.format(group_name="unreal.group"),
            ]
        ),
        " ".join(
            [
                "--no-interpreter-init",
                EXEC_COMMAND_FMT.format(
                    group_name="unreal.group", entry_point="42", raw_data="asdf"
                ),
            ]
        ),
    ],
)
def test_no_interpreter(loader, cmd):
    """
    Test that the library can handle a user which have forgotten to
    initialize the embedded python interpreter.

    Do:
        run the loader with the --no-interpreter-init flag.

    Expect:
        1) The loader binary has failed (exit code isn't 0).
        2) There is the following output:
            "Python interpreter is not initialized. Please create a py::scoped_interpreter."
    """
    EXPECTED_OUTPUT = "Python interpreter is not initialized. Please create a py::scoped_interpreter.\n"

    command: list[str] = shlex.split(" ".join([str(loader), cmd]))
    completed = subprocess.run(command, capture_output=True, check=False)

    assert completed.returncode == 1
    assert len(completed.stdout) == 0
    assert completed.stderr.decode("ascii") == EXPECTED_OUTPUT


@requires_installed_package("example")
def test_list_plugins_find_entry_point(loader):
    """
    Test that the library is able to find & load entry points.

    :note:
        This test assumes that the example-package is installed in the environment.
        without this package there will be no entry-point to be found in the example.group.
        It will be assumed that the example-package is installed & it installs 2
        entry-points in the example.group and their names are:
        1) hello
        2) 42

    Do:
        1) Run the loader list command on the example.group group.
    Expect:
        1) The loader binary has succeeded (exit code is 0).
        2) The entry point named 42 is printed.
        3) The entry point named hello isn't printed (didn't passed the filtering)
    """
    ALLOWLIST = ("42",)
    DENYLIST = ("hello",)

    command: list[str] = shlex.split(
        " ".join([str(loader), LIST_COMMAND_FMT.format(group_name="example.group")])
    )
    completed = subprocess.run(command, capture_output=True, check=False)
    stdout = completed.stdout.decode("ascii")

    assert completed.returncode == 0
    assert len(completed.stderr) == 0
    assert all((denied not in stdout for denied in DENYLIST))
    assert all((allowed in stdout for allowed in ALLOWLIST))


@pytest.mark.parametrize(
    "entry_point_output", [("example.group", "42", b"asdf")], indirect=True
)
@requires_installed_package("example")
def test_invoke_loaded_entry_point(loader, entry_point_output):
    """
    Test that the library is able to find, load & invoke entry points.

    :note:
        This test assumes that the example-package is installed in the environment.
        without this package there will be no entry-point to be found in the example.group.
        It will be assumed that the example-package is installed & it installs 2
        entry-points in the example.group and their names are:
        1) hello
        2) 42

    Do:
        1) Run the loader exec command on the example.group group and entry point named 42
           with input "asdf".
    Expect:
        1) The loader binary has succeeded (exit code is 0).
        2) The output of the loader includes the output of the entry-point.
        3) The output of the loader ends with the result of the entry-point.
    """
    command: list[str] = shlex.split(
        " ".join(
            [
                str(loader),
                EXEC_COMMAND_FMT.format(
                    group_name="example.group", entry_point="42", raw_data="asdf"
                ),
            ]
        )
    )
    completed = subprocess.run(command, capture_output=True, check=False)
    stdout = completed.stdout.decode("ascii")
    result = stdout.replace(entry_point_output.stdout, "").replace("\n", "")

    assert completed.returncode == 0
    assert len(completed.stderr) == 0
    assert entry_point_output.stdout in stdout
    assert entry_point_output.result.decode("ascii") == result
