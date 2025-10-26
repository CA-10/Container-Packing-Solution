from abc import ABC, abstractmethod
from Visualisation.Visualisation_Object import Visualisation_Object

"""
This is an abstract class which is used as the base class for all visualisation classes.
The visualise_best_member() method renders the best member
"""

class Visualisation_Base(ABC):
    
    @abstractmethod
    def visualise(self, visualisation_object, generation=None):
        pass