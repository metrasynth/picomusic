from .stage import Stage
from .sunvoxsource import inprocess_sunvox_source

_GLOBAL_PLAYER = None


class Player:

    def __init__(self):
        self.source = inprocess_sunvox_source()
        self.pyglet_player = self.source.play()
        self.performance = self.new_stage()
        self.audition = self.new_stage()
        self.ui_sounds = self.new_stage()

    def new_stage(self):
        return Stage(self.source.sunvox)


def global_player():
    global _GLOBAL_PLAYER
    if _GLOBAL_PLAYER is None:
        _GLOBAL_PLAYER = Player()
    return _GLOBAL_PLAYER
