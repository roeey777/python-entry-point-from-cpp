"""
Implementation of the integration tests for the library.
"""

import functools
import shlex
import subprocess
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Callable, Optional

import pytest
from _pytest.fixtures import SubRequest as RequestFixture
from pytest import CaptureFixture

LIST_COMMAND_FMT = "list --group-name {group_name}"
EXEC_COMMAND_FMT = (
    "exec --group-name {group_name} --entry-point {entry_point} {raw_data}"
)


@dataclass
class EntryPointOutput:
    stdout: str
    stderr: str
    result: bytes


def requires_installed_package(package_name: str) -> Callable:
    """
    A decorator for skipping a test if the given package isn't installed.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:  # noqa: ANN401
            _ = pytest.importorskip(package_name)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@pytest.fixture
def entry_point_output(
    request: RequestFixture, capsys: CaptureFixture,
) -> Optional[EntryPointOutput]:
    """
    Capture the output of a given entry point (the arguments are taken from request.param)
    """
    group_name: str
    entry_point_name: str
    data: str
    group_name, entry_point_name, data = request.param
    entry_points: metadata.EntryPoints = metadata.entry_points()
    group_entries = entry_points.select(group=group_name)
    filtered_entry_points = [
        ep.load() for ep in group_entries if ep.name == entry_point_name
    ]

    if len(filtered_entry_points) == 0:
        return None

    entry_point = filtered_entry_points[0]
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
            ],
        ),
        " ".join(
            [
                "--no-interpreter-init",
                EXEC_COMMAND_FMT.format(
                    group_name="unreal.group",
                    entry_point="42",
                    raw_data="asdf",
                ),
            ],
        ),
    ],
)
def test_no_interpreter(loader: Path, cmd: str) -> None:
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
def test_list_plugins_find_entry_point(loader: Path) -> None:
    """
    Test that the library is able to find & load entry points.

    :note:
        This test assumes that the example-package is installed in the environment.
        without this package there will be no entry-point to be found in the example.group.
        It will be assumed that the example-package is installed & it installs 3
        entry-points in the example.group and their names are:
        1) hello
        2) 42
        3) 666

    Do:
        1) Run the loader list command on the example.group group.
    Expect:
        1) The loader binary has succeeded (exit code is 0).
        2) The entry points named 42 & 666 are printed.
        3) The entry point named hello isn't printed (didn't passed the filtering)
    """
    ALLOWLIST = (
        "42",
        "666",
    )
    DENYLIST = ("hello",)

    command: list[str] = shlex.split(
        " ".join([str(loader), LIST_COMMAND_FMT.format(group_name="example.group")]),
    )
    completed = subprocess.run(command, capture_output=True, check=False)
    stdout = completed.stdout.decode("ascii")

    assert completed.returncode == 0
    assert len(completed.stderr) == 0
    assert all(denied not in stdout for denied in DENYLIST)
    assert all(allowed in stdout for allowed in ALLOWLIST)


@requires_installed_package("example")
@pytest.mark.parametrize(
    "entry_point_output",
    [("example.group", "42", b"asdf")],
    indirect=True,
)
def test_invoke_loaded_entry_point(
    loader: Path, entry_point_output: Optional[EntryPointOutput],
) -> None:
    """
    Test that the library is able to find, load & invoke entry points.

    :note:
        This test assumes that the example-package is installed in the environment.
        without this package there will be no entry-point to be found in the example.group.
        It will be assumed that the example-package is installed & it installs 3
        entry-points in the example.group and their names are:
        1) hello
        2) 42
        3) 666

    Do:
        1) Run the loader exec command on the example.group group and entry point named 42
           with input "asdf".
    Expect:
        1) The loader binary has succeeded (exit code is 0).
        2) The output of the loader includes the output of the entry-point.
        3) The output of the loader ends with the result of the entry-point.
    """
    assert entry_point_output is not None

    command: list[str] = shlex.split(
        " ".join(
            [
                str(loader),
                EXEC_COMMAND_FMT.format(
                    group_name="example.group",
                    entry_point="42",
                    raw_data="asdf",
                ),
            ],
        ),
    )
    completed = subprocess.run(command, capture_output=True, check=False)
    stdout = completed.stdout.decode("ascii")
    result = stdout.replace(entry_point_output.stdout, "").replace("\n", "")

    assert completed.returncode == 0
    assert len(completed.stderr) == 0
    assert entry_point_output.stdout in stdout
    assert entry_point_output.result.decode("ascii") == result


@requires_installed_package("example")
def test_invoke_malfunctioning_entry_point(loader: Path) -> None:
    """
    Test that the library is able to handle exceptions raised from loaded
    entry-points

    :note:
        This test assumes that the example-package is installed in the environment.
        without this package there will be no entry-point to be found in the example.group.
        It will be assumed that the example-package is installed & it installs 3
        entry-points in the example.group and their names are:
        1) hello
        2) 42
        3) 666

    Do:
        1) Run the loader exec command on the example.group group and entry point named 666
           with input "asdf".
    Expect:
        1) The loader binary has fails (exit code is 1).
        2) There is no output from the loader (in stdout).
        3) The output (stderr) of the loader contains an error message regarding
           a failure in the invoked plugin.
    """
    EXPECTED_ERROR_MSG_PREFIX = "Caught an exception from python, which is:"
    EXPECTED_EXCEPTION = "RuntimeError: Nobody expects the Spanish inquisition!"

    command: list[str] = shlex.split(
        " ".join(
            [
                str(loader),
                EXEC_COMMAND_FMT.format(
                    group_name="example.group",
                    entry_point="666",
                    raw_data="asdf",
                ),
            ],
        ),
    )
    completed = subprocess.run(command, capture_output=True, check=False)
    stderr = completed.stderr.decode("ascii")

    assert completed.returncode == 1
    assert len(completed.stdout) == 0
    assert stderr.startswith(EXPECTED_ERROR_MSG_PREFIX)
    assert EXPECTED_EXCEPTION in stderr
