import sys

import begin
import pyglet
from IPython import start_ipython
from traitlets.config import get_config

from picomusic import __version__

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


BANNER = f'Welcome to PicoMusic v{__version__}!\n'


@begin.start
@begin.logging
def main():
    c = get_config()
    c.InteractiveShellApp.exec_lines = [
        '%gui pyglet',
    ]
    c.InteractiveShell.banner2 = BANNER
    c.InteractiveShell.confirm_exit = False
    c.InteractiveShellApp.display_banner = True
    start_ipython(config=c)
