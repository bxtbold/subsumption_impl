from threading import Event
from typing import List


class Behavior:
    def __init__(self, name, check_condition, action, priority):
        """
        Represents a single behavior in the subsumption architecture.

        :param name: Name of the behavior
        :param check_condition: Function to check if the behavior should execute
        :param action: Function to execute when the behavior is active
        :param priority: Priority level of the behavior (higher = more priority)
        """
        self.name = name
        self.check_condition = check_condition
        self.action = action
        self.priority = priority
        self.active = False

    def execute(self):
        """Check condition and execute action if true."""
        if self.check_condition():
            self.active = True
            self.action()
        else:
            self.active = False


class Subsumption:
    def __init__(self, stop_event: Event):
        self.behaviors: List[Behavior] = []
        self.stop_event = stop_event

    def add_behavior(self, behavior: Behavior):
        """Add a behavior to the architecture."""
        self.behaviors.append(behavior)
        self.behaviors.sort(key=lambda b: b.priority, reverse=True)

    def run(self):
        """Run the subsumption architecture loop."""
        while not self.stop_event.is_set():
            for behavior in self.behaviors:
                behavior.execute()
                if behavior.active:
                    break  # Subsumes lower-priority behaviors
