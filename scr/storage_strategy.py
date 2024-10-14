from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    """abstract class to set the methods for the storag strategy"""
    @abstractmethod
    def save(self, habit):
        pass

    @abstractmethod
    def load(self, habit_id):
        pass

    @abstractmethod
    def delete(self, habit_id):
        pass