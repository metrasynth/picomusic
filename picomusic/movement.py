from collections import namedtuple
from fractions import Fraction
from math import ceil

from .note import Note

WHOLE_NOTE_TICKS = 192

PlacedNote = namedtuple('PlacedNote', 'measure beat part notes')


class Movement:

    def __init__(self, signature='4/4', measures=None):
        self.notes = []
        self.measure_length, self.beat_length = signature.split('/')
        self.measure_length = int(self.measure_length)
        self.beat_length = Fraction(f'1/{self.beat_length}')
        self.bar_note_length = self.beat_length * self.measure_length
        self._measures = measures

    def __iter__(self):
        return iter(self.notes)

    def place(self, measure, beat, part, notes):
        if isinstance(notes, Note):
            notes = [notes]
        self.notes.append(PlacedNote(measure, beat, part, notes))

    def placed_note_on_tick(self, n) -> int:
        return int((
            n.measure * self.bar_note_length +
            n.beat * self.beat_length
        ) * WHOLE_NOTE_TICKS)

    def placed_note_off_tick(self, n) -> int:
        max_length = max(nn.length for nn in n.notes)
        return int(
            self.placed_note_on_tick(n) +
            max_length * WHOLE_NOTE_TICKS
        )

    @property
    def signature(self):
        return f'{self.measure_length}/{self.beat_length.denominator}'

    @property
    def parts(self) -> set:
        p = set()
        for placed in self.notes:
            p.add(placed.part)
        return p

    @property
    def measure_ticks(self) -> int:
        ticks = self.measure_length * self.beat_length * WHOLE_NOTE_TICKS
        assert ticks.denominator == 1, 'Signature not compatible with 48 PQN'
        return int(ticks)

    @property
    def measures(self) -> int:
        if self._measures is not None:
            return self._measures
        if len(self.notes) == 0:
            return 0
        positions = reversed(sorted(
            (n.measure, n.beat, max(nn.length for nn in n.notes))
            for n in self.notes
        ))
        last_measure, last_beat, max_length = next(positions)
        extra_measures = last_beat * self.beat_length + max_length
        if extra_measures <= 1.0:
            extra_measures = 0
        return max(1, last_measure + ceil(extra_measures))

    @property
    def ticks(self) -> int:
        return int(self.measures * self.bar_note_length * WHOLE_NOTE_TICKS)
