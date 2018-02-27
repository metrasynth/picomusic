import sys

import begin
from IPython import start_ipython
from traitlets.config import get_config

from picomusic import __version__


# Make audio playback more responsive than default Pyglet setting of 1 or 2 seconds.
if sys.platform != 'win32':
    from pyglet.media.drivers.openal.adaptation import OpenALAudioPlayer11
    OpenALAudioPlayer11._ideal_buffer_size = 0.1
else:
    from pyglet.media.drivers.directsound.interface import DirectSoundBufferFactory
    DirectSoundBufferFactory.default_buffer_size = 0.5


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
