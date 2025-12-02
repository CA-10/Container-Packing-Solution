from Algorithms.AlgorithmBase import AlgorithmBase as AB
from Algorithms.GA.Member_Cartesian import Member_Cartesian
import time
from Algorithms.Container_Context import Container_Context
import math

class Algorithm_Random(AB):
    
    def __init__(self, radii: list[float], masses: list[int], container_width: int, container_height: int, max_iterations: int):
        self.current = None
        self.best = None
        self.best_fitness = -math.inf
        self.radii = radii
        self.masses = masses
        self.num_circles = len(radii)
        self.container_width = container_width
        self.container_height = container_height
        self.max_iterations = max_iterations
    
    def generate_random_solution(self) -> None:
        #Reusing the Member class because it implements everything we need
        container_context = Container_Context(self.container_width, self.container_height)
        self.current = Member_Cartesian(self.radii, self.masses, container_context, self.num_circles)
    
    def evaluate_current_solution(self) -> float:
        if self.current == None:
            return 0.0
        
        return self.current.calculate_fitness()
    
    def run(self) -> None:
        start_time = time.time()
        
        for i in range(self.max_iterations):
            self.generate_random_solution()
            fitness = self.evaluate_current_solution()
            
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best = self.current
            
            print(f"Generation: {i}")
            print(f"Fitness: {fitness}")
            print(f"Best Fitness: {self.best_fitness}")
            
            self.num_iterations_or_generations = i
            
            if fitness == 1.0:
                break
        
        end_time = time.time()
        self.runtime_seconds = end_time - start_time
        self.fitness = self.best_fitness
        
        self.print_stats()