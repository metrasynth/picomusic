from rv.modules.module import Module

from ..tunings import equal_temperament


class Voice:

    default_tuning = equal_temperament

    def sunvox_module(self) -> Module:
        raise NotImplemented()

    def audition(self, notes, player=None):
        from picomusic.movement import Movement
        from picomusic.note import Note
        from picomusic.part import Part
        from picomusic.player import global_player
        if isinstance(notes, Note):
        if isinstance(notes, (Note, str)):
            notes = [notes]
        player = player or global_player()
        stage = player.audition
        pitches = self.default_tuning.pitches
        notes = [
            Note(pitches[note]) if isinstance(note, str) else note
            for note in notes
        ]
        part = Part(self)
        movement = Movement()
        for note in notes:
            movement.place(0, 0, part, note)
        stage.timeline.clear()
        stage.timeline.place(0, 0, movement)
        stage.play_once()
