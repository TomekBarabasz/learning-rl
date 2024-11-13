from abc import ABC,abstractmethod

class environment(ABC):
    @abstractmethod
    def get_info(self):
        raise NotImplementedError
    abstractmethod
    def reset_to_random(self):
        raise NotImplementedError
    abstractmethod
    def initialize(self, *state):
        raise NotImplementedError
    abstractmethod
    def step(self, *actions):
        raise NotImplementedError