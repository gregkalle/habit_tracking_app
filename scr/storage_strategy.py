"""
NAME
    storage_strategy

DESCRIPTION
    Contains the abstract class StorageStrategy

CLASSES
    ABC
        StorageStrategy
"""
from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    """abstract class to set the methods for the storag strategy"""
    @abstractmethod
    def save(self, habit):
        """save the habit"""

    @abstractmethod
    def load(self, habit_id):
        """load the habit"""

    @abstractmethod
    def delete(self, habit_id):
        """delete the habit"""
