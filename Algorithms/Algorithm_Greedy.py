import random
from Algorithms.AlgorithmBase import AlgorithmBase as AB
import math
from Algorithms.Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Algorithms.Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Algorithms.Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import Algorithms.Operators.penalty_functions as penalty_functions
import Algorithms.Operators.placement_functions as placement_functions
from Algorithms.Vector2 import Vector2
from Algorithms.Container_Context import Container_Context

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
        sorted_pairs = sorted(zip(self.masses, self.radii), reverse=True)
        self.masses = [m for m, _ in sorted_pairs]
        self.radii = [r for _, r in sorted_pairs]

        self.placed_circles = []
        self.placed_masses = []

        self.placed_circles, self.placed_masses = placement_functions.place_circles(self.radii, self.masses, self.container_context)
        
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

        penalty = (10.0 * p1) + (10.0 * p2) + (0.5 * p3) + (1.6 * p4)
        #fitness = math.exp(-0.001 * penalty)
        fitness = -penalty
        
        return fitness
        
if __name__ == "__main__":
    c = Container_Context(30, 15)
    a = Algorithm_Greedy(c, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300])
    #a = Algorithm_Greedy(200, 200, 200, [random.randint(2, 10) for _ in range(15)], [random.randint(100, 2500) for _ in range(15)])
    a.run()

    print(a.placed_circles)

    pos = []

    for i in a.placed_circles:
        pos.append((i[0], i[1]))

    com = [0, 0]
    #com = penalty_functions.calculate_com_penalty(a.placed_circles, a.masses, Vector2(a.container_width / 2, a.container_height / 2))[0]
    cb = Visualisation_Object(pos, a.radii, a.masses, com, a.container_context.container_width, a.container_context.container_height)

    print(a.calculate_fitness())

    c = Custom_Visualisation()
    c.visualise(cb)