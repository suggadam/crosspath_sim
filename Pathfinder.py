# Pathfinder class;
# Capable of navigating a grid-matrix of different resistances to find a path of least-resistance.
#
class Pathfinder:
    def __init__(self, grid_map: list[list[int]], ) -> None:
        self.grid_map = grid_map