from collections import namedtuple

PlacedPhrase = namedtuple('PlacedPhrase', 'x y phrase')


class Timeline:
    """A collection of all timed elements used in a composition."""

    def __init__(self):
        self.phrases = []

    def __iter__(self):
        return iter(self.phrases)

    def clear(self):
        """Remove all phrases from the timeline."""
        self.phrases.clear()

    def place(self, phrase, x=None, y=None):
        """
        Place a note on the timeline.
        :param phrase:
        :param x: Starting tick for phrase; None to place at end.
        :param y: Y position to place phrase; None to find open space.
        """
        if x is None:
            if self.phrases:
                p = self.final_phrases[0]
                x = p.x + p.phrase.ticks
            else:
                x = 0
        if y is None:
            y = 0  # TODO: place where it won't overlap any existing phrases
        self.phrases.append(PlacedPhrase(x, y, phrase))

    @property
    def final_phrases(self) -> list:
        """Return list of phrases that end at the last tick of the timeline."""
        final = []
        max_tick = 0
        for placed in self.phrases:
            end_tick = placed.x + placed.phrase.ticks
            if end_tick > max_tick:
                final.clear()
                max_tick = end_tick
            if end_tick == max_tick:
                final.append(placed)
        return final

    @property
    def parts(self) -> set:
        """Return a set of Parts used across all phrases."""
        p = set()
        for placed in self:
            p.update(placed.phrase.parts)
        return p
