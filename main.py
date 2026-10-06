import numpy as np


class Agent:
    def __init__(self,
                 uid: int,
                 home_coords: tuple[int, int],
                 work_coords: tuple[int, int],
                 max_instructions_length: int,
                 pos_log_cap: int):
        self.uid = uid
        self.x = home_coords[0]
        self.y = home_coords[1]
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
            self.target_dest_queue = self.target_dest_queue[1:]
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
                print(symbol, end="    ")
            print("\n")

    def set_index_value(self, x, y, value) -> bool:
        if x >= 0 and x < self.map_width and y >= 0 and y < self.map_height:
            self.map_matrix[x][y] = value
            return True
        else:
            return False




class Simulation:
    def __init__(self,
                 sim_map: SimMap,
                 agents: list[Agent]):
        self.sim_map = sim_map
        self.agents = agents
        self.agents_awaiting_instructions: list[Agent] = agents
        self.agents_with_instructions: list[Agent] = []
        self.agents_waiting: list[Agent] = []

    def pathfind(self, current_coords: tuple[int, int], target_coords: tuple[int, int]) -> list[tuple[int, int]]:
        move_instructions = []
        print("pathfind")
        return move_instructions

    # Iterate through three categories of agent, in separate lists:
    # Firstly, agents awaiting their move-instructions. These will pathfind then take a step.
    # Secondly, agents with move-instructions. These will take a step then check if they've completed their commute.
    # Thirdly, agents that are waiting. These will check if their wait is complete; transfer to awaiting-instructions.
    def tick(self):
        for agent in self.agents:
            agent.log()

        # Call pathfind for agents with no instructions
        for agent in self.agents_awaiting_instructions:
            agent.take_new_move_instructions(
                self.pathfind((agent.x, agent.y), agent.target_dest_queue[0])
            )
            agent.move_step()

        # Iterate through move instructions of agents until termination instruction (0,0)
        for agent in self.agents_with_instructions:
            if (agent.move_instructions_queue[0] == (0, 0)):
                agent.wait_time = 10 # a placeholder until queued coord->wait->coord->wait implemented
                self.agents_with_instructions.remove(agent)
                self.agents_waiting.append(agent)
            else:
                agent.move_step()

        #for agent











def main():
    agent = Agent(0, (0, 0), (100, 100), 100, 1000)
    agent.take_new_move_instructions([(1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)])
    for i in range(15):
        agent.move_step()
        print(agent.x, agent.y)
        agent.update_target_dest_queue()

    sim_map = SimMap(20, 20)
    sim_map.print_map()



if __name__ == '__main__':
    main()