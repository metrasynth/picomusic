from .sunvoxproject import project_from_timeline
from .timeline import Timeline


class Stage:
    def __init__(self, sunvox):
        self.slot = sunvox.Slot()
        self.timeline = Timeline()

    def play_once(self):
        project = project_from_timeline(self.timeline)
        with open('/tmp/foo.sunvox', 'wb') as f:
            project.write_to(f)
        self.slot.load(project)
        self.slot.play_from_beginning()
        self.slot.set_autostop(True)
