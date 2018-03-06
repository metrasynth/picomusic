from rv.api import NOTECMD, Pattern, Project

EMPTY = NOTECMD.EMPTY
NOTE_OFF = NOTECMD.NOTE_OFF
SET_PITCH = NOTECMD.SET_PITCH


def project_from_timeline(timeline):
    project = Project()
    # 120 BPM, 48 ticks per quarter note
    project.initial_bpm = 120 * 2
    project.initial_tpl = 1
    voice_modules = dict(
        (voice, voice.sunvox_module())
        for voice in
        set(part.voice for part in timeline.parts)
    )
    modules = list(voice_modules.values())
    project += modules
    project.output << modules
    for placed_movement in timeline:
        movement = placed_movement.movement
        ticks = movement.ticks
        for i, part in enumerate(movement.parts):
            pattern = Pattern(
                tracks=16,
                x=placed_movement.x,
                y=placed_movement.y + i * 10,
                lines=ticks,
            )
            project += pattern
            reserved = set()
            module = voice_modules[part.voice]
            mm = module.index + 1
            for placed_note in movement:
                if placed_note.part is part:
                    start_tick = movement.placed_note_on_tick(placed_note)
                    stop_tick = movement.placed_note_off_tick(placed_note)
                    for nn in placed_note.notes:
                        track = 0
                        while (start_tick, track) in reserved:
                            track += 1
                            assert track < 16, \
                                f'Track overflow at {start_tick}'
                        cell = pattern.data[start_tick][track]
                        cell.note = SET_PITCH
                        cell.val = nn.pitch.sp_value
                        cell.module = mm
                        for tick in range(start_tick, stop_tick + 1):
                            if tick < ticks:
                                reserved.add((tick, track))
                        if stop_tick < ticks:
                            cell = pattern.data[stop_tick][track]
                            cell.note = NOTE_OFF
    return project
