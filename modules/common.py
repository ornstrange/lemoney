from typing import TypedDict, IO, Callable

class ModuleOptions(TypedDict):
    fs: IO[str]
    """Output stream module should write to"""
    notify: Callable[..., None]
    """Function to call when there is new data"""

