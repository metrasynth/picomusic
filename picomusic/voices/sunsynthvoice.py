import py
from rv.api import read_sunvox_file
from rv.modules.module import Module

from .voice import Voice

SUNSYNTH_BASE_PATH = py.path.local(__file__).dirpath()


class SunsynthVoice(Voice):

    sunsynth_filename = None

    def sunvox_module(self) -> Module:
        if self.sunsynth_filename:
            filename = str(SUNSYNTH_BASE_PATH / self.sunsynth_filename)
            return read_sunvox_file(filename).module
        else:
            raise ValueError('sunsynth_filename must be set')
