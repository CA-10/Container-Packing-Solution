from AlgorithmBase import AlgorithmBase as AB
import math
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import random
from GA.Member import Member

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
            potential_wasted_space_penalties = []
            
            for candidate in valid_candidates_stage1:
                potential_com = self.calculate_potential_com(candidate, m)
                dist = self.dist(potential_com, (self.container_width / 2, self.container_height / 2))
                potential_com_distances.append(dist)
                potential_wasted_space_penalties.append(self.calculate_touching_penalty(candidate, r))
            
            #Sort the candidates by their distance from COM. Add the candidate with the lowest distance
            potential_com_distances, valid_candidates_stage1 = zip(*sorted(zip(potential_com_distances, valid_candidates_stage1), reverse=False))
            valid_candidates_stage2.append(valid_candidates_stage1[0])
            
            #Now sort the candidates by the wasted space.
            potential_wasted_space_penalties, valid_candidates_stage2 = zip(*sorted(zip(potential_wasted_space_penalties, valid_candidates_stage2), reverse=False))

            if valid_candidates_stage2:
                #Pick random valid candidate so that solution is not always the same
                best_position = valid_candidates_stage2[0]
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
                for angle in self.linspace(0, 2 * math.pi, 50):
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
    
    def calculate_touching_penalty(self, new_circle, new_circle_r, desired_distance_factor=2.4):
        #Penalize circles which are not touching their neighbours. This will help reduce wasted space.
        penalty = 0
        
        for i in range(len(self.placed_circles)):
            dx = self.placed_circles[i][0] - new_circle[0]
            dy = self.placed_circles[i][1] - new_circle[1]
            dist = math.sqrt(dx**2 + dy**2)
            
            desired_distance = (self.radii[i] + new_circle_r) * desired_distance_factor
            
            #Only penalize if circles are too far apart (don't interfere with overlaps)
            if dist > desired_distance:
                penalty += (dist - desired_distance) ** 2
                    
        return penalty
    
    def calculate_fitness(self):
        #Convert the circles into a Member to use the class's built in fitness methods.
        positions = []
        radii = []
        
        for (x, y, r) in self.placed_circles:
            positions.append((x, y))
            radii.append(r)
        
        member = Member(self.container_width, self.container_height, len(positions))
        member.genome = positions
        
        penalty = 0
        penalty += member.calculate_overlap(radii) * 1.3
        penalty += member.calculate_bounds_overlap(radii) * 1.0
        penalty += member.calculate_com_penalty(self.placed_masses, [self.container_width / 2, self.container_height / 2])[1] * 1.0
        penalty += member.calculate_touching_penalty(radii) * 1.0

        fitness = 1 / (1 + penalty)
        
        return fitness
        
    def dist(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

a = Algorithm_Greedy(20, 15, 10, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500])
#a = Algorithm_Greedy(200, 200, 200, [random.randint(2.0, 10) for _ in range(200)], [random.randint(100, 2500) for _ in range(200)])
a.run()

print(a.placed_circles)

pos = []

for i in a.placed_circles:
    pos.append((i[0], i[1]))

com = a.calculate_com()
cb = Visualisation_Object(pos, a.radii, a.masses, com, a.container_width, a.container_height)

print(a.calculate_fitness())

c = Custom_Visualisation()
c.visualise(cb)