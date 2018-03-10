class Part:
    """A part of a composition, which may have a name and a certain voice."""

    def __init__(self, voice=None, name=None):
        self.voice = voice
        self.name = name

    def __repr__(self):
        if self.name:
            return f'<Part name={repr(self.name)} voice={repr(self.voice)}>'
        else:
            return f'<Part id={hex(id(self))} voice={repr(self.voice)}>'
