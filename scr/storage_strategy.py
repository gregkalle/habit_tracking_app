from abc import ABC, abstractmethod

class StorageStrategy(ABC):

    @abstractmethod
    def save(self, habit_complition_manager):
        pass

    @abstractmethod
    def load(self, manager_id):
        pass