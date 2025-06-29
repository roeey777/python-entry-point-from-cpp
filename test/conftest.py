"""
conftest.py - a collection of fixtures & definitions for pytest (auto-loaded).
"""

import logging
from pathlib import Path

import pytest
from pytest import Config, Parser


def pytest_addoption(parser: Parser) -> None:
    """
    Add the --loader cli option in order to tell pytest where the loader binary
    is located.
    """
    parser.addoption("--loader", action="store", default="build/test/loader")


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    return logging.getLogger("test_integration")


@pytest.fixture(scope="session")
def loader_path(pytestconfig: Config) -> Path:
    """
    a fixture which holds the path to the loader binary.
    """
    return Path(pytestconfig.getoption("loader"))


@pytest.fixture
def loader(loader_path: Path, logger: logging.Logger) -> Path:
    if not loader_path.exists():
        logger.error("Loader can't be found at: %s", str(loader_path))
        pytest.skip()

    return loader_path
