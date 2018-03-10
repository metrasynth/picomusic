"""Note lengths, expressed in terms of multiples of 4/4 measures."""

from fractions import Fraction as F

double_whole = F(2)
whole = double_whole / 2
half = whole / 2
quarter = half / 2
eighth = quarter / 2
sixteenth = eighth / 2
thirty_second = sixteenth / 2
sixty_fourth = thirty_second / 2


def dotted(length):
    """A note that is 1.5 times its original length."""
    return length * F('3/2')


def triplet(length):
    """A note that is 2/3 times its original length."""
    return length * F('2/3')


__all__ = [
    'dotted',
    'double_whole',
    'eighth',
    'half',
    'quarter',
    'sixteenth',
    'sixty_fourth',
    'thirty_second',
    'triplet',
    'whole',
]
