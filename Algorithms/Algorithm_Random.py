import random
from AlgorithmBase import AlgorithmBase as AB
from GA.Member import Member
from Visualisation.Custom_Visualisation import Custom_Visualisation
from Visualisation.Visualisation_Object import Visualisation_Object
import time

class Algorithm_Random(AB):
    
    def __init__(self, radii, masses, container_width, container_height, num_circles, max_iterations):
        self.current = None
        self.best = None
        self.best_fitness = 0
        self.radii = radii
        self.masses = masses
        self.num_circles = num_circles
        self.container_width = container_width
        self.container_height = container_height
        self.max_iterations = max_iterations
    
    def generate_random_solution(self):
        #Reusing the Member class because it implements everything we need
        self.current = Member(self.container_width, self.container_height, self.num_circles)
    
    def evaluate_current_solution(self):
        if self.current == None:
            return
        
        penalty = 0
        penalty += self.current.calculate_overlap(self.radii)
        penalty += self.current.calculate_bounds_overlap(self.radii)
        penalty += self.current.calculate_com_penalty(self.masses, [50, 50])[1]

        fitness = 1 / (1 + penalty)
        
        return fitness
    
    def run(self):
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
        
        
#====TODO Remove, this is just testing code.====
a = Algorithm_Random([random.randint(2, 10) for _ in range(5)], [random.randint(2, 100) for _ in range(5)], 100, 100, 5, 1000)

a.run()


best_member = a.best

com = best_member.calculate_com_penalty(a.masses, [a.container_width / 2, a.container_height / 2])[0]
cb = Visualisation_Object(best_member.genome, a.radii, a.masses, com, a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)