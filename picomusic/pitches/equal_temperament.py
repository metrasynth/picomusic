from .pitch import Pitch


def _names_octaves():
    for octave in range(10):
        for name in 'C,C#,D,D#,E,F,F#,G,G#,A,A#,B'.split(','):
            yield name, octave


def _pitch_item(name, octave, sp_value):
    p = Pitch(name, octave, sp_value)
    return p.label, p


_sp_values = range(0x7800, -1, -0x100)

pitches = dict(
    _pitch_item(name, octave, sp_value)
    for (name, octave), sp_value
    in zip(_names_octaves(), _sp_values)
)
