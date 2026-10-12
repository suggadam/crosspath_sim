from random import randint
from Agent import Agent
from GridMap import GridMap
from Pathfinder import Pathfinder


class Simulation:
    def __init__(self,
                 grid_map: GridMap,
                 agents: list[Agent],
                 max_instructions_length: int):
        self.current_tick = 0
        self.grid_map = grid_map
        self.pathfinder = Pathfinder(self.grid_map, max_instructions_length)
        self.agents = agents
        # Create copy of references-list to agents, to be appended and removed between the logic-lists
        self.agents_awaiting_instructions: list[Agent] = list(agents)
        self.agents_with_instructions: list[Agent] = []
        self.agents_waiting: list[Agent] = []
        self.max_instructions_length = max_instructions_length

    # Iterate through three categories of agent, in separate lists:
    # Firstly, agents awaiting their move-instructions. These will pathfind then take a step.
    # Secondly, agents with move-instructions. These will take a step then check if they've completed their commute.
    # Thirdly, agents that are waiting. These will check if their wait is complete; transfer to awaiting-instructions.
    def tick(self):
        print("\nPerforming tick")

        # Log state of all agents at the start of the tick
        print("0. Logging all agent positions")
        for agent in self.agents:
            agent.perform_log()

        # Call pathfind for agents with no instructions
        print(f"1. Creating move-instructions for all awaiting agents [{len(self.agents_awaiting_instructions)}]")
        for agent in list(self.agents_awaiting_instructions):
            agent.receive_move_instructions(
                self.pathfinder.beeline_pathfind(agent.current_coords, agent.target_destination_queue[0])
            )
            self.agents_awaiting_instructions.remove(agent)
            self.agents_with_instructions.append(agent)

        # Iterate through move instructions of agents until termination instruction (0,0)
        print(f"2. Performing move-instruction step for all active agents [{len(self.agents_with_instructions)}]")
        for agent in list(self.agents_with_instructions):
            if agent.current_coords == agent.target_destination_queue[0]:
                # Target reached; therefore, set new target
                agent.advance_target_destination_queue()
                agent.wait_time = 10 # a placeholder until queued coord->wait->coord->wait implemented
                self.agents_with_instructions.remove(agent)
                self.agents_waiting.append(agent)
            elif agent.move_instructions[0] == (0, 0): # Ran out of instructions
                self.agents_awaiting_instructions.append(agent)
                self.agents_with_instructions.remove(agent)
            else:
                agent.step()

        print(f"3. Performing wait-tick for all waiting agents [{len(self.agents_waiting)}]")
        for agent in list(self.agents_waiting):
            agent.wait()
            if agent.wait_time <= 0:
                self.agents_waiting.remove(agent)
                self.agents_awaiting_instructions.append(agent)

        self.current_tick += 1

        print("\n")











def main():
    print("Hello World")
    # Declare and define simulation variables
    max_num_of_ticks = 1000
    grid_width = 100
    grid_height = 100
    grid_map = GridMap(grid_width, grid_height)
    num_agents = 100
    max_instructions_length = 10
    log_cap = 1000
    print("Initializing agents")
    agents = [Agent(i,
                    (randint(0, grid_width), randint(0, grid_height)),
                    (randint(0, grid_width), randint(0, grid_height)),
                    (randint(0, grid_width), randint(0, grid_height)),
                     max_instructions_length,
                     log_cap) for i in range(num_agents)]


    print("Starting simulation")
    simulation = Simulation(grid_map, agents, max_instructions_length)

    for i in range(max_num_of_ticks):
        print(f"Tick #{i}")
        simulation.tick()
        if i % 33 == 0:
            for agent in agents[0:10]:
                print(f"Agent #{agent.uid}:"
                      f"\tx={agent.current_coords[0]},"
                      f"\ty={agent.current_coords[1]},"
                      f"\twait={agent.wait_time}"
                      f"\thome={agent.HOME_COORDS},"
                      f"\twork={agent.WORK_COORDS}")
                print(agent.log)
                print(agent.move_instructions)






if __name__ == '__main__':
    main()