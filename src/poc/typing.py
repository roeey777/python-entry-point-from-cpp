"""
Typing annotations for POC's Plugins (entry points)
"""

from collections.abc import Callable

Plugin = Callable[[bytes], bytes]
