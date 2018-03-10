from rv.api import NOTECMD, Project

from .sunvoxproject import project_from_timeline
from .timeline import Timeline


class Stage:
    """
    Organizes related aspects of a performance.

    :ivar slot: SunVox playback slot used to render audio.
    :ivar timeline: Timeline used to organize performance events.
    """

    def __init__(self, sunvox) -> None:
        self.slot = sunvox.Slot()
        self.timeline = Timeline()

    def play_once(self) -> None:
        """Play the performance one time."""
        self.stop(reset=True)
        self.slot.load(self.sunvox_project)
        self.slot.set_autostop(True)
        self.slot.play_from_beginning()

    def play(self) -> None:
        """Play the performance in a continuous loop."""
        self.stop(reset=True)
        self.slot.load(self.sunvox_project)
        self.slot.set_autostop(False)
        self.slot.play_from_beginning()

    def stop(self, reset=False) -> None:
        """
        Stop the performance, optionally resetting audio engine.
        :param reset: Forcibly reset audio engine if True.
        """
        reset = reset or self.stopped
        self.slot.stop()
        if reset:
            self.slot.send_event(0, NOTECMD.CLEAN_SYNTHS, 0, 0, 0, 0)

    @property
    def playing(self) -> bool:
        """Is the performance playing?"""
        return not self.stopped

    @property
    def stopped(self) -> bool:
        """Is the performance stopped?"""
        return self.slot.end_of_song()

    @property
    def sunvox_project(self) -> Project:
        """The Rendered SunVox project for this stage's timeline."""
        return project_from_timeline(self.timeline)
