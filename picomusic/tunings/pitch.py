from rv.api import NOTE, NOTECMD


class Pitch:
    """A pitch in a scale or note in a drum kit.

    :ivar name: Name given to the pitch.
    :ivar octave: Octave of the pitch.
    :ivar sunvox_note: SunVox note for the pitch; None if sp_value set.
    :ivar sp_value: SunVox SP value for the pitch; None if sunvox_note set.
    """

    def __init__(self, name, octave, sunvox_note_or_sp_value):
        self.name = name
        self.octave = octave
        if isinstance(sunvox_note_or_sp_value, (NOTE, NOTECMD)):
            self.sunvox_note = sunvox_note_or_sp_value
            self.sp_value = None
        else:
            self.sunvox_note = None
            self.sp_value = sunvox_note_or_sp_value

    @property
    def label(self):
        """Label based on name, or name and octave."""
        return f'{self.name}{self.octave or ""}'

    def __repr__(self):
        return f'<Pitch name={repr(self.name)} octave={self.octave} ' \
               f'sp_value={hex(self.sp_value)}>'
