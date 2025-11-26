import random
from Algorithms.AlgorithmBase import AlgorithmBase as AB
from Algorithms.GA.Population_Cartesian import Population_Cartesian
from Algorithms.Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Algorithms.Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Algorithms.Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import time
from Algorithms.Operators.penalty_functions import *
from Algorithms.Container_Context import Container_Context

class Algorithm_GA(AB):
    
    def __init__(self, max_generations: int, population_size: int, mutation_rate: float, container_width: int, container_height: int, radii: list[float], masses: list[int], selection_method:str="roulette", tournament_size:int=3):
        self.gen_count = 0
        self.max_generations = max_generations
        self.population_size = population_size
        self.container_width = container_width
        self.container_height = container_height
        self.radii = radii
        self.masses = masses
        self.best_fitnesses = []
        self.selection_method = selection_method
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        
        self.container_context = Container_Context(container_width, container_height)
        self.population = Population_Cartesian(population_size, self.container_context, radii, masses)
    
    def run(self) -> None:
        start_time = time.time()
        
        for gen in range(self.max_generations):
            max_fitness = self.run_generation()  
            self.best_fitnesses.append(max_fitness)
            
            print(f"Generation: {gen}")
            print(f"Best Fitness: {max_fitness}")
            print(f"Average Fitness: {sum(self.population.fitnesses) / len(self.population.fitnesses)}")
            
            self.gen_count += 1
            self.num_iterations_or_generations += 1
            
            if max_fitness == 1.0:
                break
        
        end_time = time.time()
        self.runtime_seconds = end_time - start_time
        self.fitness = self.population.calculate_fitness()
        
        self.print_stats()
            
    def run_generation(self) -> float:
        best = self.population.calculate_fitness()

        temp_population = []

        while len(temp_population) < self.population_size:
            if self.selection_method == "roulette":
                parent_a = self.population.roulette_wheel_selection()
                parent_b = self.population.roulette_wheel_selection()
            elif self.selection_method == "tournament":
                parent_a = self.population.tournament_selection(self.tournament_size)
                parent_b = self.population.tournament_selection(self.tournament_size)
            else:
                raise Exception(f"{self.selection_method} not a valid selection method")

            child1, child2 = self.population.crossover(parent_a, parent_b)
            temp_population.extend([child1, child2])

        self.population.population = temp_population[:self.population_size]
        self.population.mutate(self.mutation_rate)

        return best

#====TODO Remove, this is just testing code.====
a = Algorithm_GA(300, 800, 0.05, 30, 15, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300], "tournament", 8)
#a = Algorithm_GA(1000, 700, 0.03, 100, 100, 1000, [random.randint(3, 15) for _ in range(15)], [random.randint(100, 2500) for _ in range(15)])



a.run()


best_member = a.population.population[a.population.fitnesses.index(max(a.population.fitnesses))].genome

positions = []
vector2positions = []

for gene in best_member:
    positions.append([gene.position.x, gene.position.y])
    vector2positions.append(gene.position)

#com = calculate_com_penalty(best_member.genome, a.masses, [a.container_width / 2, a.container_height / 2])[0]
com = [0, 0]
cb = Visualisation_Object(positions, a.radii, a.masses, com, a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)

Results_Graphs.draw_fitness_over_gens(a.best_fitnesses)