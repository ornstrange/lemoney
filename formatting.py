def attribute(attribute: str, text: str) -> str:
    """Set the attribute for the following text."""
    return f"%{{+{attribute}}}{text}%{{-{attribute}}}"

def foreground(color: str, text: str) -> str:
    """Set the text foreground color."""
    return f"%{{F{color}}}{text}%{{F-}}"

def background(color: str, text: str) -> str:
    """Set the text background color."""
    return f"%{{B{color}}}{text}%{{B-}}"

def font(index: int, text: str) -> str:
    """Set the font used to draw the following text."""
    return f"%{{T{index}}}{text}%{{T-}}"

def underline(color: str, text: str) -> str:
    """Set the text underline color."""
    return f"%{{U{color}}}{text}%{{U-}}"

def action(action: str, text: str) -> str:
    """Create a clickable area starting from the current position."""
    return f"%{{A:{action}:}}{text}%{{A}}"

def monitor(monitor: str, text: str) -> str:
    """Change the monitor the bar is rendered to."""
    return f"%{{S{monitor}}}{text}"

def offset(offset: int) -> str:
    """Offset the current position by pixels in the alignment direction."""
    return f"%{{O{offset}}}"

def reverse() -> str:
    """Swap the current background and foreground colors."""
    return "%{R}"

def reversed(text: str) -> str:
    """Swap the current background and foreground colors."""
    return f"%{{R}}{text}%{{R}}"

def left(text: str) -> str:
    """Aligns the following text to the left side of the screen."""
    return f"%{{l}}{text}"

def center(text: str) -> str:
    """Aligns the following text to the center of the screen."""
    return f"%{{c}}{text}"

def right(text: str) -> str:
    """Aligns the following text to the right side of the screen."""
    return f"%{{r}}{text}"

def line_over(text: str) -> str:
    """Draw a line over the text."""
    return attribute('o', text)

def line_under(text: str) -> str:
    """Draw a line under the text."""
    return attribute('u', text)

