# The Agent object;
# Input -> home-coordinates: tuple(x, y), workplace-coordinates: tuple(x, y)
# Holds relevant coordinates and
class Agent:
    def __init__(self,
                 home_coords: tuple[int, int],
                 work_coords: tuple[int, int],
                 maximum_move_instruction_length: int):
        self.home_coords = home_coords
        self.work_coords = work_coords
        self.current_coords = (home_coords[0], home_coords[1])
        self.move_instructions = [(0,0)] * maximum_move_instruction_length
        self.wait_time = 0

    # Function called each tick
    def move(self, new_coords: tuple[int, int]):
        # Update coordinates with move-instructions; tuples of two -1s, 0s, and/or 1s, referring to axial adjustment
        if self.move_instructions[0] != (0, 0):
            self.current_coords[0] += self.move_instructions[0][0] # Adjust x-coordinate
            self.current_coords[1] += self.move_instructions[0][1] # Adjust y-coordinate
        # Update instructions
        self.move_instructions = self.move_instructions[1:]
        self.move_instructions.append((0, 0))


    # Function called to wait agent [remove from active list, add to waiting list]
    # Once wait is complete, returns 0 [remove from waiting list, add to active list]
    def wait_tick(self):
        if self.wait_time == 0:
            return 0
        else:
            self.wait_time -= 1

    # Provides agent with new move-instructions to iterate through at each time-step
    # Overrides old move-instructions with new; after last new index, iterates once to add termination 0, 0 tuple.
    def add_move_instructions(self, new_move_instructions: list[tuple[int, int]]):
        assert len(new_move_instructions) <= len(self.move_instructions)

        i = 0
        while i < len(new_move_instructions):
            self.move_instructions[i] = new_move_instructions[i]
            i += 1
        if i < len(self.move_instructions):
            self.move_instructions[i] = (0, 0) # Set termination at index after last instruction



    def get_current_coords(self):
        return self.current_coords

    def get_home_coords(self):
        return self.home_coords

    def get_work_coords(self):
        return self.work_coords




# Finds quickest path from starting position to goal (distance * resistance).
# Using JPS, Jump Point Search.
# Returns a list of (x, y) coordinates as instructions to follow.
# Function must only be called once per commute.
# Memory usage is dynamic; must implement limitation (i.e. maximum # of steps allowable as function of map size)
def pathfind(map_matrix: list[list[int]],
             starting_coords: tuple[int, int],
             goal_coords: tuple[int, int]) -> list[tuple[int, int]]:
    print("pathfinding")
    return [(0,0)]




def print_map(map_matrix: list[list[int]]):
    for row in map_matrix:
        print(row)




# def print_map_with_agents():

# def print_map_with_agent_and_path




# Time step;
# Input -> tick: int - used to determine what logic to perform.
# Operate on a tick-by-tick basis.
# Midnight/New-day at tick 0; scales timely events in accordance to ticks-in-day.
def time_step(tick: int, ticks_in_day: int, ):
    print("tick", tick)




# Generate an empty matrix of the world
def generate_world(WORLD_MAX_X: int, WORLD_MAX_Y: int) -> list[list[int]]:
    # Ints represent move-speed restriction; 0 is unrestricted. 100 is uncommutable (a wall).
    world = [[0 for i in range(WORLD_MAX_X)] for i in range(WORLD_MAX_Y)]

    return world



# Generate the list of default-agents
def generate_agents(num_of_agents: int) -> list[Agent]:
    list_of_agents = []

    for i in range(num_of_agents):
        list_of_agents.append(Agent((0, 0), (10, 10), 1000))

    return list_of_agents




def main():
    print("Hello World")

    # Take user input for parameters of world and agents
    WORLD_MAX_X = 1000
    WORLD_MAX_Y = 1000
    NUM_OF_AGENTS = 1
    MAX_NUM_OF_TICKS = 10000
    duration_of_day_in_ticks = 86400 # If 1-tick = 1-second then 86400-ticks = 24-hours


    # Call functions to generate world and agents
    world_matrix = generate_world(WORLD_MAX_X, WORLD_MAX_Y)
    list_of_agents = generate_agents(NUM_OF_AGENTS)



    print_map(world_matrix)


if __name__ == '__main__':
    main()