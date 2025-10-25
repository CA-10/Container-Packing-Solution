from abc import ABC, abstractmethod

"""
This is an abstract class which is used as the base class for all visualisation classes.
The visualise_best_member() method renders the best member
"""

class Visualisation_Base(ABC):
    
    @abstractmethod
    def visualise_best_member(self, best_member, population, generation=None):
        pass