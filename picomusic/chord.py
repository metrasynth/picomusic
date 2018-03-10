from fractions import Fraction

from .note import Note
from .tunings import equal_temperament
from .voices import PIANO


class Chord:

    def __init__(self, pitches, length='1/4', tuning=equal_temperament):
        pitches = [
            tuning.pitches[pitch] if isinstance(pitch, str) else pitch
            for pitch in pitches
        ]
        self.pitches = pitches
        self.length = Fraction(length)

    def __repr__(self):
        return f"Chord(pitches={repr(self.pitches)}, length='{self.length}'>"

    @property
    def notes(self):
        return [Note(pitch, self.length) for pitch in self.pitches]

    def audition(self, voice=PIANO):
        voice.audition(self.notes)
