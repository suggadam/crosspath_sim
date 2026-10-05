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
        self.target_coords = (0, 0)
        # To-do-queue:
        self.target_dest_queue: list[tuple[int, int]] = [home_coords, work_coords]
        self.move_instructions: list[tuple[int, int]] = [(0,0)] * max_instructions_length
        self.wait_time = 0
        self.pos_log = [(0, 0)] * pos_log_cap # Updates one element per tick in the simulation

    def log(self):
        self.pos_log.append((self.x, self.y))

    def update_target_dest_queue(self):
        self.target_dest_queue = self.target_dest_queue[1:] + self.target_dest_queue[:1]

    # Instructions should be verified before use
    def move_step(self) -> bool:
        if self.move_instructions[0] != (0, 0):
            # Translate current position to new position with instructions
            self.x += self.move_instructions[0][0]
            self.y += self.move_instructions[0][1]
            # Update instruction, deleting used instruction and appending empty instruction
            self.move_instructions = self.move_instructions[1:]
            self.move_instructions.append((0, 0))
            return True
        else:
            return False

    def take_new_move_instructions(self,
                              new_instructions: list[tuple[int, int]]) -> bool:

        def _verify_move_instruction_legality(instruction: tuple[int, int]) -> bool:
            if instruction[0] < -1 or instruction[0] > 1 or instruction[1] < -1 or instruction[1] > 1:
                return False
            else:
                return True

        if len(new_instructions) <= len(self.move_instructions):
            i = 0
            while i < len(new_instructions):
                # Ensure instruction is legal; if not, cuts instruction short.
                if _verify_move_instruction_legality(new_instructions[i]):
                    self.move_instructions[i] = new_instructions[i]
                    i += 1
                else:
                    i = len(new_instructions)
            # Set termination
            if i < len(new_instructions):
                self.move_instructions[i] = (0, 0)
            return True
        else:
            return False

    def wait_tick(self):
        if self.wait_time >= 1:
            self.wait_time -= 1
            return True
        else:
            return False


class Map:
    def __init__(self,
                 map_width: int,
                 map_height: int):
        self.map_width = map_width
        self.map_height = map_height



class Simulation:
    def __init__(self,
                 map: Map,
                 agents: list[Agent]):
        self.map = map
        self.agents = agents
        self.agents_awaiting_instructions: list[Agent] = agents
        self.agents_with_instructions: list[Agent] = []
        self.agents_waiting: list[Agent] = []

    def pathfind(self, current_coords: tuple[int, int], target_coords: tuple[int, int]) -> list[tuple[int, int]]:

    # Iterate through three categories of agent, in separate lists:
    # Firstly, agents awaiting their move-instructions. These will pathfind then take a step.
    # Secondly, agents with move-instructions. These will take a step then check if they've completed their commute.
    # def tick(self):
    #     for agent in self.agents_awaiting_instructions:







def main():
    agent = Agent(0, (0, 0), (100, 100), 100, 1000)
    agent.take_new_move_instructions([(1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)])
    for i in range(100):
        agent.move_step()
        print(agent.x, agent.y)
        agent.update_target_dest_queue()

if __name__ == '__main__':
    main()