import time
from threading import Thread, Event
from subsumption import Subsumption, Behavior


class DummyRobot:
    def __init__(self, stop_event) -> None:
        self.robot_state = {
            "is_interrupted": False,
            "is_collided": False,
            "is_potential_collision": False,
            "is_within_constraints": True
        }
        self.subsumption = Subsumption(stop_event)

    def set_robot_state(self, name, value):
        if name in self.robot_state:
            self.robot_state[name] = value

    def register_behaviors(self):
        # Create behaviors with priorities
        interrupt_behavior = Behavior(
            "Interrupt",
            self.is_interrupted,
            self.handle_interruption,
            priority=4
        )
        collision_behavior = Behavior(
            "Collision",
            self.is_collided,
            self.handle_collision,
            priority=3
        )
        potential_collision_behavior = Behavior(
            "PotentialCollision",
            self.is_potential_collision,
            self.handle_potential_collision,
            priority=2
        )
        constraint_behavior = Behavior(
            "Constraints",
            self.is_within_constraints,
            self.maintain_constraints,
            priority=1
        )

        # Add each behavior to subsumption
        self.subsumption.add_behavior(interrupt_behavior)
        self.subsumption.add_behavior(collision_behavior)
        self.subsumption.add_behavior(potential_collision_behavior)
        self.subsumption.add_behavior(constraint_behavior)

    # Monitoring conditions
    def is_interrupted(self):
        return self.robot_state["is_interrupted"]

    def is_collided(self):
        return self.robot_state["is_collided"]

    def is_potential_collision(self):
        return self.robot_state["is_potential_collision"]

    def is_within_constraints(self):
        return self.robot_state["is_within_constraints"]

    # Behavior actions
    def handle_interruption(self):
        print("[Behavior] Handling interruption...")

    def handle_collision(self):
        print("[Behavior] Collision detected! Stopping manipulator.")

    def handle_potential_collision(self):
        print("[Behavior] Adjusting path to avoid collision.")

    def maintain_constraints(self):
        print("[Behavior] Operating within constraints.")


if __name__ == "__main__":
    stop_event = Event()

    dummy_robot = DummyRobot(stop_event)
    dummy_robot.register_behaviors()

    def subsumption_loop(robot: DummyRobot):
        while not stop_event.is_set():
            robot.subsumption.run()
            time.sleep(0.1)

    thread = Thread(target=subsumption_loop, args=(dummy_robot,), daemon=True)
    thread.start()

    # Simulate state changes for testing
    time.sleep(1)
    dummy_robot.set_robot_state("is_within_constraints", False)
    time.sleep(1)
    dummy_robot.set_robot_state("is_potential_collision", True)
    time.sleep(1)
    dummy_robot.set_robot_state("is_collided", True)
    time.sleep(1)
    dummy_robot.set_robot_state("is_interrupted", True)
    time.sleep(1)

    # Stop the architecture after testing
    stop_event.set()
    thread.join()

    print("Subsumption architecture stopped.")
