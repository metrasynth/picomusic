from collections import namedtuple
from fractions import Fraction
from math import ceil, floor

from .lengths import quarter
from .note import Note

WHOLE_NOTE_TICKS = 192

PlacedNote = namedtuple('PlacedNote', 'measure beat part notes')


class Phrase:
    """A musical phrase with a common time signature."""

    def __init__(self, signature='4/4', measures=None):
        """
        Create a Phrase.

        :param signature: String of time signature, '/' separated.
        :param measures: Fixed number of measures; None for automatic.
        """
        self.notes = []
        self.measure_length, self.beat_length = signature.split('/')
        self.measure_length = int(self.measure_length)
        self.beat_length = Fraction(f'1/{self.beat_length}')
        self.bar_note_length = self.beat_length * self.measure_length
        self._measures = measures

    def __iter__(self):
        return iter(self.notes)

    def place(self, measure, beat, part, notes, length=quarter):
        """
        :param measure: Measure number to place the note into.
        :param beat: Fraction of a 4/4 measure to place the note at.
        :param part: The part that will voice the notes.
        :param notes: Note or list of notes to place.
        :param length: Length of notes that are specified as strings.
        """
        if isinstance(notes, (Note, str)):
            notes = [notes]
        extra_measures = floor(beat * 4 / self.measure_length)
        measure += extra_measures
        beat -= extra_measures * self.measure_length / 4
        notes = [
            (Note(part.voice.default_tuning.pitches[note], length=length)
             if isinstance(note, str)
             else note)
            for note in notes
        ]
        self.notes.append(PlacedNote(measure, Fraction(beat), part, notes))

    def placed_note_on_tick(self, n) -> int:
        """
        :type n: PlacedNote
        :return: tick where n's on event occurs.
        """
        return int(
            (n.measure * self.bar_note_length + n.beat * self.beat_length * 4)
            * WHOLE_NOTE_TICKS
        )

    def placed_note_off_tick(self, n) -> int:
        """
        :type n: PlacedNote
        :return: tick where n's off event occurs.
        """
        max_length = max(nn.length for nn in n.notes)
        return int(
            self.placed_note_on_tick(n) +
            max_length / 4 * WHOLE_NOTE_TICKS
        )

    @property
    def signature(self):
        """
        :return: String representation of the time signature.
        """
        return f'{self.measure_length}/{self.beat_length.denominator}'

    @property
    def parts(self) -> set:
        """
        :return: Set of unique Parts used by all notes in this phrase.
        """
        p = set()
        for placed in self.notes:
            p.add(placed.part)
        return p

    @property
    def measure_ticks(self) -> int:
        """
        :return: Number of ticks used by each measure in this phrase.
        """
        ticks = self.measure_length * self.beat_length * WHOLE_NOTE_TICKS
        assert ticks.denominator == 1, 'Signature not compatible with 48 PQN'
        return int(ticks)

    @property
    def measures(self) -> int:
        """
        :return: Number of measures in this phrase.
        """
        if self._measures is not None:
            return self._measures
        if len(self.notes) == 0:
            return 0
        positions = reversed(sorted(
            (n.measure, n.beat, max(nn.length for nn in n.notes))
            for n in self.notes
        ))
        last_measure, last_beat, max_length = next(positions)
        extra_measures = last_beat + max_length
        return max(1, last_measure + ceil(extra_measures))

    @property
    def ticks(self) -> int:
        """
        :return: Number of ticks in this phrase.
        """
        return int(self.measures * self.bar_note_length * WHOLE_NOTE_TICKS)
