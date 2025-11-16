import random
from AlgorithmBase import AlgorithmBase as AB
import math
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import Operators.penalty_functions as penalty_functions
import Operators.placement_functions as placement_functions
from Vector2 import Vector2
from Container_Context import Container_Context

class Algorithm_Greedy(AB):

    def __init__(self, container_context: Container_Context, radii: list[float], masses: list[int]):
        if len(radii) != len(masses):
            raise ValueError("radii and masses must be of same length")
        
        self.container_context = container_context
        self.masses = masses
        self.radii = radii
        self.placed_circles = []
        self.placed_masses = []
        self.masks = [1 for _ in range(len(radii))]
        self.remaining_capacity = self.container_context.container_mass_limit
    
    def run(self) -> None:
        #Sort by mass ascending for greedy because we can fit more containers in without exceeding the weight limit
        sorted_pairs = sorted(zip(self.masses, self.radii, self.masks), reverse=False)
        self.masses = [m for m, _, _ in sorted_pairs]
        self.radii = [r for _, r, _ in sorted_pairs]
        self.masks = [s for _, _, s in sorted_pairs]

        self.placed_circles = []
        self.placed_masses = []

        self.placed_circles, self.placed_masses, self.placed_masks = placement_functions.place_circles(self.radii, self.masses, self.masks, self.container_context, self.container_context.container_mass_limit)
        
    def calculate_fitness(self) -> float:
        positions = []
        radii = []
        
        for (x, y, r) in self.placed_circles:
            positions.append(Vector2(x, y))
            radii.append(r)
                
        p1 = penalty_functions.calculate_overlap_penalty(positions, self.placed_masks, radii)
        p2 = penalty_functions.calculate_bounds_overlap_penalty(positions, self.placed_masks, radii, self.container_context.container_width, self.container_context.container_height)
        p3 = penalty_functions.calculate_com_penalty(positions, self.placed_masks, self.placed_masses, Vector2(self.container_context.container_width / 2, self.container_context.container_height / 2))[1]
        p4 = penalty_functions.calculate_packing_fitness(positions, radii, self.placed_masks)
        p5 = penalty_functions.knapsack_term(self.placed_masses, self.placed_masks, self.container_context.container_mass_limit)

        penalty = (10.0 * p1) + (10.0 * p2) + (0.5 * p3) + (1.6 * p4) + (15.0 * 0)
        fitness = math.exp(-0.001 * penalty)
        
        return fitness
        
if __name__ == "__main__":
    c = Container_Context(20, 15, 5000)
    a = Algorithm_Greedy(c, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500])
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