from fractions import Fraction

from .tunings import equal_temperament
from .voices import PIANO


class Note:

    def __init__(self, pitch, length='1/4'):
        if isinstance(pitch, str):
            pitch = equal_temperament.pitches[pitch]
        self.pitch = pitch
        self.length = Fraction(length)

    def __repr__(self):
        return f"Note(pitch={repr(self.pitch.label)}, length='{self.length}'>"

    def audition(self, voice=PIANO):
        voice.audition(self)
