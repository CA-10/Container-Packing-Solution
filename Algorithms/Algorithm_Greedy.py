from AlgorithmBase import AlgorithmBase as AB
import math
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import random

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
        #Sort by mass descending as bigger masses influence COM more so place them first.
        self.masses, self.radii = zip(*sorted(zip(self.masses, self.radii), reverse=True))
        self.placed_circles = []

        for r, m in zip(self.radii, self.masses):
            candidate_positions = self.generate_candidate_positions(r)
            valid_candidates_stage1 = [p for p in candidate_positions if not self.does_overlap(p, r)]
            valid_candidates_stage2 = []
            
            potential_com_distances = []
            
            for candidate in valid_candidates_stage1:
                potential_com = self.calculate_potential_com(candidate, m)
                dist = self.dist(potential_com, (self.container_width / 2, self.container_height / 2))
                potential_com_distances.append(dist)
            
            #Sort the candidates by their distance from COM. Add the candidate with the lowest distance
            potential_com_distances, valid_candidates_stage1 = zip(*sorted(zip(potential_com_distances, valid_candidates_stage1), reverse=False))
            valid_candidates_stage2.append(valid_candidates_stage1[0])

            if valid_candidates_stage2:
                #Pick random valid candidate so that solution is not always the same
                best_position = random.choice(valid_candidates_stage2)
                self.placed_circles.append((best_position[0], best_position[1], r))
                self.placed_masses.append(m)
            else:
                print(f"No valid placement found for radius {r}")


    def generate_candidate_positions(self, circle_r):
        candidate_positions = []

        #If haven't placed any circles yet, place the circle at the center of the container
        if not self.placed_circles:
            candidate_positions.append((self.container_width / 2, self.container_height / 2))
        else:
            for (x, y, r) in self.placed_circles:
                for angle in self.linspace(0, 2 * math.pi, 36):
                    new_x = x + (circle_r + r) * math.cos(angle)
                    new_y = y + (circle_r + r) * math.sin(angle)
                    
                    if (circle_r <= new_x <= self.container_width - circle_r and
                        circle_r <= new_y <= self.container_height - circle_r):
                        candidate_positions.append((new_x, new_y))
                        
        return candidate_positions

    def does_overlap(self, circle_position, circle_r):
        for (x, y, r) in self.placed_circles:
            dx = circle_position[0] - x
            dy = circle_position[1] - y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < (r + circle_r):
                return True
                
        return False

    def linspace(self, start, stop, num):
        if num == 1:
            return [start]
        step = (stop - start) / (num - 1)
        return [start + i * step for i in range(num)]
    
    def calculate_com(self):
        com = [0, 0]
        sum_mx = 0
        sum_my = 0
        total_mass = sum(self.masses)
        
        for i in range(len(self.placed_circles)):
            circle = (self.placed_circles[i][0], self.placed_circles[i][1])
            circle_x = circle[0]
            circle_y = circle[1]
            circle_mass = self.masses[i]
            
            sum_mx += circle_x * circle_mass
            sum_my += circle_y * circle_mass

        com[0] = sum_mx / total_mass
        com[1] = sum_my / total_mass
        
        return com
        
    def calculate_potential_com(self, new_circle, m):
        com = [0, 0]
        sum_mx = 0
        sum_my = 0
        total_mass = sum(self.placed_masses) + m
        
        for i in range(len(self.placed_masses)):
            circle = (self.placed_circles[i][0], self.placed_circles[i][1])
            circle_x = circle[0]
            circle_y = circle[1]
            circle_mass = self.masses[i]
            
            sum_mx += circle_x * circle_mass
            sum_my += circle_y * circle_mass
        
        sum_mx += new_circle[0] * m
        sum_my += new_circle[1] * m

        com[0] = sum_mx / total_mass
        com[1] = sum_my / total_mass
        
        return com
        
    def dist(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

a = Algorithm_Greedy(20, 15, 7, [2.0, 2.0, 1.5, 1.5, 1.2, 1.5, 1.2], [2500, 2500, 800, 800, 300, 800, 300])
a.run()

print(a.placed_circles)

pos = []

for i in a.placed_circles:
    pos.append((i[0], i[1]))

com = a.calculate_com()
cb = Visualisation_Object(pos, a.radii, a.masses, com, a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)