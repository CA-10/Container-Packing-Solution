import random
from AlgorithmBase import AlgorithmBase as AB
import math
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
from Operators.penalty_functions import *
from Operators.placement_funcs import *

class Algorithm_Greedy(AB):

    def __init__(self, container_width, container_height, num_circles, radii, masses):
        self.container_width = container_width
        self.container_height = container_height
        self.num_circles = num_circles
        self.masses = masses
        self.radii = radii
        self.placed_circles = []
        self.placed_masses = []
    
    def run(self):
        #Sort by mass descending
        sorted_pairs = sorted(zip(self.masses, self.radii), reverse=True)
        self.masses = [m for m, _ in sorted_pairs]
        self.radii = [r for _, r in sorted_pairs]
            
        self.placed_circles = []
        self.placed_masses = []

        self.placed_circles, self.placed_masses = place_circles(self.radii, self.masses, self.container_width, self.container_height)
        
    def calculate_fitness(self):
        positions = []
        radii = []
        
        for (x, y, r) in self.placed_circles:
            positions.append((x, y))
            radii.append(r)
                
        penalty = calculate_total_penalty(positions, radii, self.masses, self.container_width, self.container_height)

        fitness = math.exp(-0.001 * penalty)
        
        return fitness
        
if __name__ == "__main__":
    a = Algorithm_Greedy(20, 15, 10, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500])
    #a = Algorithm_Greedy(200, 200, 200, [random.randint(2, 10) for _ in range(15)], [random.randint(100, 2500) for _ in range(15)])
    a.run()

    print(a.placed_circles)

    pos = []

    for i in a.placed_circles:
        pos.append((i[0], i[1]))

    com = calculate_com_penalty(a.placed_circles, a.masses, [a.container_width / 2, a.container_height / 2])[0]
    cb = Visualisation_Object(pos, a.radii, a.masses, com, a.container_width, a.container_height)

    print(a.calculate_fitness())

    c = Custom_Visualisation()
    c.visualise(cb)