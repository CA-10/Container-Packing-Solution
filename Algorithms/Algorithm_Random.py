from AlgorithmBase import AlgorithmBase as AB
from GA.Member_Cartesian import Member_Cartesian
from Visualisation.Custom_Visualisation import Custom_Visualisation
from Visualisation.Visualisation_Object import Visualisation_Object
import time
from Container_Context import Container_Context
import math

class Algorithm_Random(AB):
    
    def __init__(self, radii: list[float], masses: list[int], container_width: int, container_height: int, num_circles: int, max_iterations: int):
        self.current = None
        self.best = None
        self.best_fitness = -math.inf
        self.radii = radii
        self.masses = masses
        self.num_circles = num_circles
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
        
        
#====TODO Remove, this is just testing code.====
a = Algorithm_Random([2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300], 20, 15, 14, 10000)

a.run()


best_member = a.best

positions = []
vector2positions = []

for gene in best_member.genome: #type: ignore
    positions.append([gene.position.x, gene.position.y])
    vector2positions.append(gene.position)

#com = calculate_com_penalty(best_member.genome, a.masses, [a.container_width / 2, a.container_height / 2])[0]
com = [0, 0]
cb = Visualisation_Object(positions, a.radii, a.masses, com, a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)