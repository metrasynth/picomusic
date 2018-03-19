import sys
from fractions import Fraction
from textwrap import indent, wrap

import begin
import pyglet
from IPython import start_ipython
from IPython.terminal.prompts import ClassicPrompts
from traitlets.config import get_config

from .. import __version__, lengths
from ..chord import Chord
from ..note import Note
from ..part import Part
from ..phrase import Phrase
from ..stagemanager import StageManager
from ..tunings import drumkit
from ..utils.terminalwidth import get_terminal_size
from ..voices import BASIC_KIT, PIANO

IDEAL_BUFFER_SIZE = 0.5


# Make audio playback more responsive than default 1+ seconds.
if sys.platform == 'win32':
    pyglet.options['audio'] = ('directsound',)
    from pyglet.media.drivers.directsound.interface import \
        DirectSoundBufferFactory
    DirectSoundBufferFactory.default_buffer_size = IDEAL_BUFFER_SIZE
else:
    pyglet.options['audio'] = ('openal',)
    from pyglet.media.drivers.openal.adaptation import OpenALAudioPlayer11
    OpenALAudioPlayer11._ideal_buffer_size = IDEAL_BUFFER_SIZE


BANNER = f'''\
Welcome to PicoMusic v{__version__}!

For your convenience, the following are available:

'''


@begin.start
@begin.logging
def main():
    def shortname(v, k):
        return getattr(v, '__name__', k).split('.')[-1]
    user_ns = {
        'BASIC_KIT': BASIC_KIT,
        'Chord': Chord,
        'F': Fraction,
        'Fraction': Fraction,
        'Note': Note,
        'PIANO': PIANO,
        'Part': Part,
        'Phrase': Phrase,
        'dotted': lengths.dotted,
        'double_whole': lengths.double_whole,
        'drumkit': drumkit,
        'eighth': lengths.eighth,
        'half': lengths.half,
        'manager': StageManager(),
        'quarter': lengths.quarter,
        'sixteenth': lengths.sixteenth,
        'sixty_fourth': lengths.sixty_fourth,
        'thirty_second': lengths.thirty_second,
        'triplet': lengths.triplet,
        'whole': lengths.whole,
    }
    c = get_config()
    c.InteractiveShellApp.exec_lines = [
        '%gui pyglet',
    ]
    c.TerminalInteractiveShell.prompts_class = ClassicPrompts
    names = ', '.join(
        k if k == shortname(v, k) else f'{k} ({shortname(v, k)})'
        for k, v in sorted(user_ns.items())
    ) + '\n'
    width, _ = get_terminal_size()
    names = '\n'.join(wrap(names, width - 5))
    names = indent(names, '    ')
    c.InteractiveShell.banner2 = BANNER + names + '\n'
    c.InteractiveShell.confirm_exit = False
    c.InteractiveShellApp.display_banner = True
    start_ipython(config=c, user_ns=user_ns)
