from collections import namedtuple

PlacedMovement = namedtuple('PlacedMovement', 'x y movement')


class Timeline:

    def __init__(self):
        self.movements = []

    def clear(self):
        self.movements.clear()

    def place(self, x, y, movement):
        self.movements.append(PlacedMovement(x, y, movement))

    def __iter__(self):
        return iter(self.movements)

    @property
    def parts(self):
        p = set()
        for placed in self:
            p.update(placed.movement.parts)
        return p
