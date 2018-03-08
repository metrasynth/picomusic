class Pitch:

    def __init__(self, name, octave, sp_value):
        self.name = name
        self.octave = octave
        self.sp_value = sp_value

    @property
    def label(self):
        return f'{self.name}{self.octave}'

    def __repr__(self):
        return f'<Pitch name={repr(self.name)} octave={self.octave} ' \
               f'sp_value={hex(self.sp_value)}'
