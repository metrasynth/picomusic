from rv.api import NOTECMD, Pattern, Project

from .timeline import Timeline

EMPTY = NOTECMD.EMPTY
NOTE_OFF = NOTECMD.NOTE_OFF
SET_PITCH = NOTECMD.SET_PITCH


def project_from_timeline(timeline: Timeline) -> Project:
    """Render a Timeline to a SunVox project."""
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
    for placed_phrase in timeline:
        p = placed_phrase.phrase
        ticks = p.ticks
        for i, part in enumerate(p.parts):
            pattern = Pattern(
                tracks=16,
                x=placed_phrase.x,
                y=placed_phrase.y + i * 10,
                lines=ticks,
            )
            project += pattern
            reserved = set()
            module = voice_modules[part.voice]
            mm = module.index + 1
            for placed_note in p:
                if placed_note.part is part:
                    start_tick = p.placed_note_on_tick(placed_note)
                    stop_tick = p.placed_note_off_tick(placed_note)
                    for nn in placed_note.notes:
                        track = 0
                        while (start_tick, track) in reserved:
                            track += 1
                            assert track < 16, \
                                f'Track overflow at {start_tick}'
                        cell = pattern.data[start_tick][track]
                        if nn.pitch.sp_value is not None:
                            cell.note = SET_PITCH
                            cell.val = nn.pitch.sp_value
                        else:
                            cell.note = nn.pitch.sunvox_note
                        cell.module = mm
                        for tick in range(start_tick, stop_tick + 1):
                            if tick < ticks:
                                reserved.add((tick, track))
                        if stop_tick < ticks:
                            cell = pattern.data[stop_tick][track]
                            cell.note = NOTE_OFF
    return project
