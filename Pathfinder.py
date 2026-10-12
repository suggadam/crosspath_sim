from GridMap import GridMap

# Pathfinder class;
# Capable of navigating a grid-matrix of different resistances to find a path of least-resistance.
#
class Pathfinder:
    def __init__(self, grid_map: GridMap, max_instructions_length: int):
        self.grid_map = grid_map
        self.max_instructions_length = max_instructions_length

    def beeline_pathfind(self, current_coords: tuple[int, int],
                         target_coords: tuple[int, int]) -> list[tuple[int, int]]:
        move_instructions = [(0, 0)] * self.max_instructions_length
        virtual_x = current_coords[0]
        virtual_y = current_coords[1]
        num_of_steps = 0

        while ((virtual_x != target_coords[0] or virtual_y != target_coords[1]) and
               num_of_steps < self.max_instructions_length):
            current_step = (0, 0)
            # Determine whether to move left or right
            if target_coords[0] < virtual_x:
                current_step = (-1, current_step[1])
            elif target_coords[0] > virtual_x:
                current_step = (1, current_step[1])
            # Determine whether to move up or down
            if target_coords[1] < virtual_y:
                current_step = (current_step[0], -1)
            elif target_coords[1] > virtual_y:
                current_step = (current_step[0], 1)

            # Update virtual coordinates
            virtual_x += current_step[0]
            virtual_y += current_step[1]
            # Add step to instructions
            move_instructions[num_of_steps] = current_step
            num_of_steps += 1

        return move_instructions