from .stage import Stage
from .sunvoxsource import inprocess_sunvox_source
from .utils.singleton import singleton


@singleton
class StageManager:
    """Manages playback of performances on stages.

    This class is a singleton.

    :ivar pyglet_player: Audio player managed by Pyglet library.
    :ivar source: Sound source, containing SunVox synth engine.
    :ivar performance: Stage used for performance of compositions.
    :ivar audition: Stage used for auditioning voices and phrases.
    :ivar ui_sounds: Stage used for user interface feedback.
    """

    def __init__(self):
        self.source = inprocess_sunvox_source()
        self.pyglet_player = self.source.play()
        self.performance = self._new_stage()
        self.audition = self._new_stage()
        self.ui_sounds = self._new_stage()

    def _new_stage(self):
        return Stage(self.source.sunvox)
