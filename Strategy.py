from abc import ABC, abstractmethod


class PathFinderStrategy(ABC):
    @abstractmethod
    def find(self, window, wait, grid, start, end):
        pass


class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def get_strategy(self):
        return self._strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def find(self, window, wait, grid, start, end):
        return self._strategy.find(window, wait, grid, start, end)
