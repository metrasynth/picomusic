"""Drum Kit note mapping."""

from rv.api import NOTE

from .pitch import Pitch

pitches = {
    'BD': Pitch('BD', None, NOTE.c4),
    'SD': Pitch('SD', None, NOTE.d4),
    'CP': Pitch('CP', None, NOTE.f4),
    'LT': Pitch('LT', None, NOTE.g4),
    'MT': Pitch('MT', None, NOTE.a4),
    'HT': Pitch('HT', None, NOTE.c5),
    'CH': Pitch('CH', None, NOTE.d5),
    'OH': Pitch('OH', None, NOTE.f5),
}
