from abc import ABC, abstractmethod

"""
This is an abstract class which is used as the base class for all algorithm classes.
The run method is the method called to run the algorithm. It is an abstract method.
"""

class AlgorithmBase(ABC):
    runtime_seconds = 0
    num_iterations_or_generations = 0
    fitness = 0
    
    @abstractmethod
    def run(self):
        pass
    
    def print_stats(self):
        print("==============Algorithm Stats==============")
        print(f"Runtime (s): {self.runtime_seconds}")
        print(f"Total Iterations/Generations: {self.num_iterations_or_generations}")
        print(f"Fitness: {self.fitness}")

        return self.runtime_seconds, self.num_iterations_or_generations, self.fitness