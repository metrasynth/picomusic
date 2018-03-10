import py
from rv.api import m, read_sunvox_file

from .voice import Voice

BASE_PATH = py.path.local(__file__).dirpath()


class SunvoxVoiceBase(Voice):

    @property
    def basename(self) -> str:
        """
        :return: Basename for the voice, based on the class name.
        """
        return self.__class__.__name__.lower()


class SunvoxVoice(SunvoxVoiceBase):

    def sunvox_module(self) -> m.Module:
        """
        :return: MetaModule based on the SunVox project for this voice.
        """
        filename = f'{BASE_PATH / self.basename}.sunvox'
        project = read_sunvox_file(filename)
        module = m.MetaModule(project=project)
        module.input_module = 1  # Assume that Note IN is module 1
        module.play_patterns = False
        return module


class SunsynthVoice(SunvoxVoiceBase):

    def sunvox_module(self) -> m.Module:
        """
        :return: Module contained in the sunsynth file for this voice.
        """
        filename = f'{BASE_PATH / self.basename}.sunsynth'
        return read_sunvox_file(filename).module
