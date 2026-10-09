import logging
from dataclasses import dataclass

class Agent:
    def __init__(self,
                 uid: int,
                 spawn_coords: tuple[int, int],
                 home_coords: tuple[int, int],
                 work_coords: tuple[int, int],
                 max_instructions_length: int,
                 log_cap: int):
        self.uid = uid
        self.current_coords: tuple[int, int] = spawn_coords
        self.HOME_COORDS = home_coords
        self.WORK_COORDS = work_coords
        self.target_destination_queue = [self.HOME_COORDS, self.WORK_COORDS]
        # A list of tuples (x, y) to be treated as translation steps, performed iteratively.
        # Static list length.
        self.move_instructions = [(0, 0)] * max_instructions_length
        self.max_instructions_length = max_instructions_length
        self.wait_time = 0
        # A log of coordinates tracked each tick
        self.log = []
        self.log_cap = log_cap

    def perform_log(self):
        if len(self.log) < self.log_cap:
            self.log.append(self.current_coords)
        else:
            print("Log cap reached")

    def step(self):
        if self.move_instructions[0] != (0, 0) and self.wait_time == 0:
            self.current_coords = (self.current_coords[0] + self.move_instructions[0][0],
                                   self.current_coords[1] + self.move_instructions[0][1])
            self.move_instructions.pop(0)
            self.move_instructions.append((0, 0))
        else:
            print(f"Agent has no move instructions {self.move_instructions[0]} or has a wait timer {self.wait_time}")

    def wait(self):
        self.wait_time -= 1
        if self.wait_time <= 0:
            self.wait_time = 0

    def receive_move_instructions(self, new_instructions: list[tuple[int, int]]):

        # Checks if the given tuple is of legal values
        def _verify_move_instruction_legality(instruction: tuple[int, int]) -> bool:
            if instruction[0] < -1 or instruction[0] > 1 or instruction[1] < -1 or instruction[1] > 1:
                return False
            else:
                return True

        for i, step in enumerate(new_instructions):

            if _verify_move_instruction_legality(step):

                # Override old instructions with new instructions
                if i < self.max_instructions_length:
                    self.move_instructions[i] = new_instructions[i]

                # Add termination/null tuple after last new instruction
                if i + 1 < self.max_instructions_length:
                    self.move_instructions[i + 1] = (0, 0)

    def advance_target_destination_queue(self):
        # Update procedure only possible if there are at least one destination in queue
        if len(self.target_destination_queue) >= 1:
            self.target_destination_queue.append(self.target_destination_queue[0])
            self.target_destination_queue.pop(0)
        else:
            print("Target destination queue is empty; cannot advance queue")

    def queue_new_target(self, new_target: tuple[int, int]):
        self.target_destination_queue.append(new_target)

    def is_at_target(self) -> bool:
        if self.current_coords == self.target_destination_queue[0]:
            return True
        else:
            return False

