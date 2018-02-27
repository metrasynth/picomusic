import begin
from IPython import start_ipython
from pyglet.media.drivers.openal.adaptation import OpenALAudioPlayer11
from traitlets.config import get_config

from picomusic import __version__


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
    OpenALAudioPlayer11._ideal_buffer_size = 0.1
    start_ipython(config=c)
