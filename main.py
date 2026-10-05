# The Agent object;
# Input -> home-coordinates: tuple(x, y), workplace-coordinates: tuple(x, y)
# Holds relevant coordinates and
class Agent:
    def __init__(self,
                 uid: int,
                 home_coords: tuple[int, int],
                 work_coords: tuple[int, int],
                 maximum_move_instruction_length: int):
        self.uid = uid
        self.home_coords = home_coords
        self.work_coords = work_coords
        self.current_coords = (home_coords[0], home_coords[1])
        self.move_instructions = [(0,0)] * maximum_move_instruction_length
        self.wait_time = 0


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

    # Function called each tick;
    # Iterates through move-instruction list, applying translation from first index to agent's coords.
    def move_one_step(self):
        # Update coordinates with move-instruction; tuples (-1/0/1, -1/0/1) representing axial translation
        # Allows diagonal movement in one-tick.
        if self.move_instructions[0] != (0, 0):
            self.current_coords[0] += self.move_instructions[0][0] # Adjust x-coordinate
            self.current_coords[1] += self.move_instructions[0][1] # Adjust y-coordinate
        else:
            return 1
        # Update instructions; delete used instruction, add empty to end.
        self.move_instructions = self.move_instructions[1:]
        self.move_instructions.append((0, 0))


    # Function called to wait agent [remove from active list, add to waiting list]
    # Once wait is complete, returns 0 [remove from waiting list, add to active list]
    def wait_tick(self):
        if self.wait_time == 0:
            return 0
        else:
            self.wait_time -= 1



# Finds quickest path from starting position to goal (distance * resistance).
# Using JPS, Jump Point Search.
# Returns a list of (x, y) coordinates as instructions to follow.
# Calls on each agent in "active-agent-list-with-no-instruction"
def pathfind(map_matrix: list[list[int]],
             starting_coords: tuple[int, int],
             goal_coords: tuple[int, int], max_num_of_steps: int) -> list[tuple[int, int]]:
    instructions = [(0, 0)] * max_num_of_steps # Static memory
    print("pathfinding")
    return []



# Time step;
# Input -> tick: int - used to determine what logic to perform.
# Operate on a tick-by-tick basis.
# Midnight/New-day at tick 0; scales timely events in accordance to ticks-in-day.
def time_step(tick: int,
              ticks_in_day: int,
              map_matrix: list[list[int]],
              active_agents_no_instructions: list[Agent],
              active_agents_with_instructions: list[Agent],
              waiting_agents: list[Agent]):
    print("tick", tick)

    for agent in active_agents_with_instructions:
        if agent.move_one_step() == 1:
            active_agents_with_instructions.remove(agent)
            active_agents_no_instructions.append(agent)

    for agent in active_agents_no_instructions:
        path = pathfind(map_matrix, )



# Generate an empty matrix of the world
def generate_world(world_max_w: int, world_max_y: int) -> list[list[int]]:
    # Ints represent move-speed restriction; 0 is unrestricted. 100 is uncommutable (a wall).
    world = [[0 for i in range(world_max_w)] for i in range(world_max_y)]

    return world



# Generate the list of default-agents
def generate_agents(num_of_agents: int) -> list[Agent]:
    list_of_agents = []

    for i in range(num_of_agents):
        list_of_agents.append(Agent(i, (0, 0), (10, 10), 1000))

    return list_of_agents


def print_map(map_matrix: list[list[int]]):
    for row in map_matrix:
        print(row)

# def print_map_with_agents():

# def print_map_with_agent_and_path

def main():
    print("Hello World")

    # Take user input for parameters of world and agents
    world_max_x = 100
    world_max_y = 100
    num_of_agents = 10
    max_num_of_ticks = 10000
    duration_of_day_in_ticks = 86400 # If 1-tick = 1-second then 86400-ticks = 24-hours

    # Call functions to generate world and agents
    world_matrix = generate_world(world_max_x, world_max_y)
    list_of_agents = generate_agents(num_of_agents)

    # Agents in this list awaiting pathfinding
    active_agent_list_no_instruction: list[Agent] = []
    # Agents in this list to perform move instructions
    active_agent_list_with_instruction: list[Agent] = []
    # Agents in this list to iterate their wait order
    waiting_agent_list: list[Agent] = []


    # Simulation Begins
    for agent in list_of_agents:
        active_agent_list_no_instruction.append(agent)


if __name__ == '__main__':
    main()
