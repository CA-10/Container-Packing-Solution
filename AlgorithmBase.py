from abc import ABC, abstractmethod

"""
This is an abstract class which is used as the base class for all algorithm classes.
The run method is the method called to run the algorithm. It is an abstract method.
"""

class AlgorithmBase(ABC):
    runtime_seconds = 0
    peak_memory_mb = 0
    num_iterations_or_generations = 0
    num_evaluations = 0
    
    @abstractmethod
    def run():
        pass