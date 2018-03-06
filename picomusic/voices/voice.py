from rv.modules.module import Module


class Voice:

    def sunvox_module(self) -> Module:
        raise NotImplemented()

    def audition(self, note, player=None):
        from picomusic.movement import Movement
        from picomusic.part import Part
        from picomusic.player import global_player
        player = player or global_player()
        stage = player.audition
        part = Part(self)
        movement = Movement()
        movement.place(0, 0, part, note)
        stage.timeline.clear()
        stage.timeline.place(0, 0, movement)
        stage.play_once()
