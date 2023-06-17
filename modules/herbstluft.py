class HerbstluftModuleOptions(ModuleOptions):
    seperator: str | None
    """Seperator between tags"""

    tiling_icons: tuple[str, str, str, str, str] | None
    """
    Icons for tiling algorithms
    ·:·      (vertical, horizontal, max,   grid,  floating)
    default: (' ∥ ',    ' ≡ ',      '[ ]', ' ┼ ', '⢐ ⢐')
    """

DefaultHerbstluftModuleOptions = {
    'seperator': ' | ',
    'tiling_icons': (' ∥ ', ' ≡ ', '[ ]', ' ┼ ', '⢐ ⢐')
}

def herbstluft_module(options: HerbstluftModuleOptions):
    """Herbstluft Module"""
    return Format.reverse() + '1' + Format.reverse() + ' | 2 | 3'

