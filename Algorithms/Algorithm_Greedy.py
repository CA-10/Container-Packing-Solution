from Algorithms.AlgorithmBase import AlgorithmBase as AB
import Algorithms.Operators.penalty_functions as penalty_functions
import Algorithms.Operators.placement_functions as placement_functions
from Algorithms.Vector2 import Vector2
from Algorithms.Container_Context import Container_Context
import time

class Algorithm_Greedy(AB):

    def __init__(self, container_context: Container_Context, radii: list[float], masses: list[int]):
        if len(radii) != len(masses):
            raise ValueError("radii and masses must be of same length")
        
        self.container_context = container_context
        self.masses = masses
        self.radii = radii
        self.placed_circles = []
        self.placed_masses = []
    
    def run(self) -> None:
        #Sort by mass descending because this will make sure the COM is central.
        start_time = time.time()
        sorted_pairs = sorted(zip(self.masses, self.radii), reverse=True)
        self.masses = [m for m, _ in sorted_pairs]
        self.radii = [r for _, r in sorted_pairs]

        self.placed_circles = []
        self.placed_masses = []

        self.placed_circles, self.placed_masses = placement_functions.place_circles(self.radii, self.masses, self.container_context)
        end_time = time.time()

        self.fitness = self.calculate_fitness()
        self.runtime_seconds = end_time - start_time
        self.num_iterations_or_generations = 1
        
    def calculate_fitness(self) -> float:
        positions = []
        radii = []
        
        for (x, y, r) in self.placed_circles:
            positions.append(Vector2(x, y))
            radii.append(r)
                
        p1 = penalty_functions.calculate_overlap_penalty(positions, radii)
        p2 = penalty_functions.calculate_bounds_overlap_penalty(positions, radii, self.container_context.container_width, self.container_context.container_height)
        p3 = penalty_functions.calculate_com_penalty(positions, self.placed_masses, Vector2(self.container_context.container_width / 2, self.container_context.container_height / 2))[1]
        p4 = penalty_functions.calculate_packing_fitness(positions, radii)

        penalty = (10.0 * p1) + (10.0 * p2) + (5.0 * p3) + (1.6 * p4)
        #fitness = math.exp(-0.001 * penalty)
        fitness = -penalty
        
        return fitness