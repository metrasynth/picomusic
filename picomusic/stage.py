from .sunvoxproject import project_from_timeline
from .timeline import Timeline


class Stage:
    def __init__(self, sunvox):
        self.slot = sunvox.Slot()
        self.timeline = Timeline()

    def play_once(self):
        self.slot.load(self.sunvox_project)
        self.slot.play_from_beginning()
        self.slot.set_autostop(True)

    @property
    def sunvox_project(self):
        return project_from_timeline(self.timeline)
