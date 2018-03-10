from rv.modules.module import Module

from ..tunings import equal_temperament


class Voice:
    """
    A distinct sound within a performance.

    :cvar default_tuning: Module
    """

    default_tuning = equal_temperament

    def sunvox_module(self) -> Module:
        """
        Override this in subclasses to return a SunVox module for the voice.
        """
        raise NotImplemented()

    def audition(self, notes):
        """
        Audition note(s) using this voice.

        :param notes: Notes to play (Note, str, or list of Note or str)
        """
        from picomusic.note import Note
        from picomusic.part import Part
        from picomusic.phrase import Phrase
        from picomusic.stagemanager import StageManager
        if isinstance(notes, (Note, str)):
            notes = [notes]
        pitches = self.default_tuning.pitches
        notes = [
            Note(pitches[note]) if isinstance(note, str) else note
            for note in notes
        ]
        manager = StageManager()
        stage = manager.audition
        part = Part(self)
        phrase = Phrase()
        for note in notes:
            phrase.place(0, 0, part, note)
        stage.timeline.clear()
        stage.timeline.place(phrase)
        stage.play_once()

    def __repr__(self):
        return f'<{self.__class__.__name__}>'
