from fractions import Fraction

from .lengths import quarter
from .tunings import equal_temperament
from .voices import PIANO


class Note:
    """The pitch and length (duration) of a musical note."""

    def __init__(self, pitch, length=quarter, tuning=equal_temperament):
        """
        Create a Note.

        :param pitch: Pitch that the note will represent.
        :param length: Length as a fraction of a 4/4 measure.
        :param tuning: Tuning to use when pitch is a str.
        """
        if isinstance(pitch, str):
            pitch = tuning.pitches[pitch]
        self.pitch = pitch
        self.length = Fraction(length)

    def __repr__(self):
        return f"<Note pitch={repr(self.pitch.label)} length='{self.length}'>"

    def audition(self, voice=PIANO):
        """
        Audition this note.

        :param voice: Voice to audition with.
        """
        voice.audition(self)
