"""Equal Temperament tuning."""

from rv.api import NOTE

from .pitch import Pitch


def _names_octaves():
    for octave in range(10):
        for name in 'C,C#,D,D#,E,F,F#,G,G#,A,A#,B'.split(','):
            yield name, octave


def _pitch_item(name, octave):
    sunvox_note = name[0].lower() if name.endswith('#') else name[0]
    note = NOTE[f'{sunvox_note}{octave}']
    p = Pitch(name, octave, note)
    return p.label, p


pitches = dict(
    _pitch_item(name, octave)
    for name, octave
    in _names_octaves()
)
