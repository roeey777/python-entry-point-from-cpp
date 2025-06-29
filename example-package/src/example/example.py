"""
An example of a package with a plugin registered via an entry-point.
"""

from poc.typing import Plugin


def hello(raw: bytes) -> bytes:
    """
    An example of a plugin, in this example there are some prints and
    the input is returned in reversed order.

    :param raw: the input of the plugin, raw bytes which can be de-serialized.
    :return: reversed order of the input bytes.
    """
    print(f"Got {len(raw)} bytes!")
    print(f"They are: {raw!r}")  # adding the !r is for decoding the raw bytes as str
    return raw[::-1]


def spanish_inquisition(raw: bytes) -> bytes:
    """
    An example of a malfunctioning plugin, in this example an exception will
    be raised.

    :param raw: the input of the plugin, raw bytes which can be de-serialized.
    :raises RuntimeError: always raises RuntimeError, for simulation of
                          a malfunctioning plugin.
    """
    raise RuntimeError("Nobody expects the Spanish inquisition!")


typed_plugin: Plugin = hello
typed_malfunctioning_plugin: Plugin = spanish_inquisition
