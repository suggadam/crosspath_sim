from random import randint

class Agent:
    def __init__(self,
                 uid: int,
                 home_coords: tuple[int, int],
                 work_coords: tuple[int, int],
                 max_instructions_length: int,
                 pos_log_cap: int):
        self.uid = uid
        self.x = randint(0, home_coords[0])
        self.y = randint(0, home_coords[1])
        self.HOME_COORDS = home_coords
        self.WORK_COORDS = work_coords
        self.target_dest_queue: list[tuple[int, int]] = [home_coords, work_coords]
        self.move_instructions_queue: list[tuple[int, int]] = [(0, 0)] * max_instructions_length
        self.wait_time = 0
        self.pos_log = [(0, 0)] * pos_log_cap # Updates one element per tick in the simulation

    def log(self):
        self.pos_log.append((self.x, self.y))

    def update_target_dest_queue(self):
        # Update procedure only possible if there are at least two destinations in queue
        if len(self.target_dest_queue) >= 2:
            self.target_dest_queue.append(self.target_dest_queue[0])
            self.target_dest_queue.pop(0)
        else:
            self.target_dest_queue = [self.HOME_COORDS, self.WORK_COORDS]

    def queue_new_target_dest(self, new_target_dest: tuple[int, int]):
        self.target_dest_queue.append(new_target_dest)

    def check_if_at_target(self) -> bool:
        if (self.x, self.y) == self.target_dest_queue[0]:
            return True
        else:
            return False


    # Performs the 0th index move-instruction; then deletes instruction
    # Instructions should be verified before use
    def move_step(self) -> bool:
        if self.move_instructions_queue[0] != (0, 0):
            # Translate current position to new position with instructions
            self.x += self.move_instructions_queue[0][0]
            self.y += self.move_instructions_queue[0][1]
            # Update instruction, deleting used instruction and appending empty instruction
            self.move_instructions_queue.pop(0)
            self.move_instructions_queue.append((0, 0))
            return True
        else:
            return False

    def take_new_move_instructions(self,
                              new_instructions: list[tuple[int, int]]) -> bool:

        # Checks if individual move-instructions are legal
        def _verify_move_instruction_legality(instruction: tuple[int, int]) -> bool:
            if instruction[0] < -1 or instruction[0] > 1 or instruction[1] < -1 or instruction[1] > 1:
                return False
            else:
                return True

        if len(new_instructions) <= len(self.move_instructions_queue):
            i = 0
            while i < len(new_instructions):
                # Ensure instruction is legal; if not, cuts instruction short.
                if _verify_move_instruction_legality(new_instructions[i]):
                    self.move_instructions_queue[i] = new_instructions[i]
                    i += 1
                else:
                    i = len(new_instructions)
            # Set termination
            if i < len(new_instructions):
                self.move_instructions_queue[i] = (0, 0)
            return True
        else:
            return False

    def wait_tick(self):
        if self.wait_time >= 1:
            self.wait_time -= 1
            return True
        else:
            return False


class SimMap:
    def __init__(self,
                 map_width: int,
                 map_height: int):
        self.map_width = map_width
        self.map_height = map_height
        self.map_matrix = [[0] * self.map_width for i in range(self.map_height)]

    def print_map(self):
        for row in range(self.map_height):
            for col in range(self.map_width):
                symbol = self.map_matrix[row][col]
                print(symbol, end=" ")
            print("\n")

    # Use to draw obstructions on map
    def set_index_value(self, x, y, value) -> bool:
        if x >= 0 and x < self.map_width and y >= 0 and y < self.map_height:
            self.map_matrix[x][y] = value
            return True
        else:
            return False




class Simulation:
    def __init__(self,
                 sim_map: SimMap,
                 agents: list[Agent],
                 max_instructions_length: int):
        self.sim_map = sim_map
        self.agents = agents
        self.agents_awaiting_instructions: list[Agent] = agents
        self.agents_with_instructions: list[Agent] = []
        self.agents_waiting: list[Agent] = []
        self.max_instructions_length = max_instructions_length

    def blank_map_pathfind(self, current_coords: tuple[int, int], target_coords: tuple[int, int]) -> list[tuple[int, int]]:
        move_instructions = [(0, 0)] * self.max_instructions_length
        virtual_x = current_coords[0]
        virtual_y = current_coords[1]
        num_of_steps = 0

        while not (virtual_x == target_coords[0] and virtual_y == target_coords[1]):
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

    # Iterate through three categories of agent, in separate lists:
    # Firstly, agents awaiting their move-instructions. These will pathfind then take a step.
    # Secondly, agents with move-instructions. These will take a step then check if they've completed their commute.
    # Thirdly, agents that are waiting. These will check if their wait is complete; transfer to awaiting-instructions.
    def tick(self):
        print("Performing tick")

        # Log state of all agents at the start of the tick
        print("0. Logging all agent positions")
        for agent in self.agents:
            agent.log()

        # Call pathfind for agents with no instructions
        print(f"1. Creating move-instructions for all awaiting agents [{len(self.agents_awaiting_instructions)}]")
        for agent in self.agents_awaiting_instructions:
            agent.take_new_move_instructions(
                self.blank_map_pathfind((agent.x, agent.y), agent.target_dest_queue[0])
            )
            agent.move_step()
            self.agents_awaiting_instructions.remove(agent)
            self.agents_with_instructions.append(agent)

        # Iterate through move instructions of agents until termination instruction (0,0)
        print(f"2. Performing move-instruction step for all active agents [{len(self.agents_with_instructions)}]")
        for agent in self.agents_with_instructions:
            if (agent.move_instructions_queue[0] == (0, 0)):
                agent.update_target_dest_queue()
                agent.wait_time = 10 # a placeholder until queued coord->wait->coord->wait implemented
                self.agents_with_instructions.remove(agent)
                self.agents_waiting.append(agent)
            else:
                agent.move_step()

        print(f"3. Performing wait-tick for all waiting agents [{len(self.agents_waiting)}]")
        for agent in self.agents_waiting:
            agent.wait_tick()
            if agent.wait_time <= 0:
                self.agents_waiting.remove(agent)
                self.agents_awaiting_instructions.append(agent)











def main():
    print("Hello World")
    # Declare and define simulation variables
    max_num_of_ticks = 1000
    map_width = 100
    map_height = 100
    sim_map = SimMap(map_width, map_height)
    num_agents = 100
    max_instructions_length = 100
    log_cap = 1000
    print("Initializing agents")
    agents = [Agent(i,
                    (randint(0, map_width), randint(0, map_height)),
                    (randint(0, map_width), randint(0, map_height)),
                     max_instructions_length,
                     log_cap) for i in range(num_agents)]


    print("Starting simulation")
    simulation = Simulation(sim_map, agents, max_instructions_length)

    for i in range(max_num_of_ticks):
        print(f"Tick #{i}")
        simulation.tick()
        if i % 100 == 0:
            for agent in agents:
                print(f"Agent #{agent.uid}:"
                      f"\tx={agent.x},"
                      f"\ty={agent.y},"
                      f"\twait={agent.wait_time}"
                      f"\thome={agent.HOME_COORDS},"
                      f"\twork={agent.WORK_COORDS}")
                print(agent.pos_log)






if __name__ == '__main__':
    main()