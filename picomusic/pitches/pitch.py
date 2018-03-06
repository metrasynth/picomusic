class Pitch:

    def __init__(self, name, octave, sp_value):
        self.name = name
        self.octave = octave
        self.sp_value = sp_value

    @property
    def label(self):
        return f'{self.name}{self.octave}'