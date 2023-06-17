class CmdModuleOptions(TypedDict):
    cmd: str
    """Command to run, path will be found and validated with shutil.which"""
    args: Iterable[str] | None
    """Arguments to cmd"""

def cmd_module(options: CmdModuleOptions):
    """Shell command Module"""
    return options['cmd']

