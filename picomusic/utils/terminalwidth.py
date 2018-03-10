"""Terminal width detection.

Based on:
- http://stackoverflow.com/questions/566746
- http://stackoverflow.com/questions/263890

TODO: be more specific with exception handling.
"""

import os
import platform
import shlex
import struct
import subprocess


def get_terminal_size():
    current_os = platform.system()
    xy = None
    if current_os == 'Windows':
        xy = _get_terminal_size_windows()
        if xy is None:
            xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        xy = _get_terminal_size_linux()
    if xy is None:
        xy = 80, 25  # default value
    return xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        STDERR = -12
        h = windll.kernel32.GetStdHandle(STDERR)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (
                bufx, bufy, curx, cury, wattr,
                left, top, right, bottom,
                maxx, maxy,
            ) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:  # noqa: E722
        pass


def _get_terminal_size_tput():
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return cols, rows
    except:  # noqa: E722
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack(
                'hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:  # noqa: E722
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:  # noqa: E722
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:  # noqa: E722
            return None
    return int(cr[1]), int(cr[0])
