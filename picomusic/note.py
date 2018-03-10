from fractions import Fraction

from .lengths import quarter
from .tunings import equal_temperament
from .voices import PIANO


class Note:

    def __init__(self, pitch, length=quarter, tuning=equal_temperament):
        if isinstance(pitch, str):
            pitch = tuning.pitches[pitch]
        self.pitch = pitch
        self.length = Fraction(length)

    def __repr__(self):
        return f"Note(pitch={repr(self.pitch.label)}, length='{self.length}'>"

    def audition(self, voice=PIANO):
        voice.audition(self)
