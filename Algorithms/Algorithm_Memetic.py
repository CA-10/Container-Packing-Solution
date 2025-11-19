import random
from AlgorithmBase import AlgorithmBase as AB
from GA.Population_OrderBased import Population_OrderBased
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import time
from Operators.penalty_functions import *
from Algorithm_Greedy import Algorithm_Greedy
from GA.Member_OrderBased import Member_OrderBased
from Container_Context import Container_Context
import Operators.placement_functions as placement_functions

class Algorithm_Memetic(AB):
    
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
        self.population = Population_OrderBased(population_size, self.container_context, radii, masses)
    
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
        # Evaluate current population
        self.population.place_members()
        best = self.population.calculate_fitness()

        # --- ELITISM ADDED HERE ---
        elite = a.population.population[a.population.fitnesses.index(max(a.population.fitnesses))]  # assumes you have such a method
        # If you don’t, replace with: elite = max(self.population.population, key=lambda m: m.fitness)
        # ---------------------------

        temp_population = [elite]  # keep elite

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

        self.population.place_members()
        best = self.population.calculate_fitness()

        return best


    """
    def local_search(self, child, max_attempts=15):
        best_genome = child.genome[:]
        best_fitness = self.population.evaluate_individual(child.genome)

        for _ in range(max_attempts):
            # create a neighbor by swapping two positions
            i, j = random.sample(range(len(best_genome)), 2)
            new_genome = best_genome[:]
            new_genome[i], new_genome[j] = new_genome[j], new_genome[i]

            new_fitness = self.population.evaluate_individual(new_genome)

            #Random is used so that local search does not always go for the best members, but allows diversity too
            if new_fitness >= best_fitness or random.random() < 0.01:
                best_genome = new_genome
                best_fitness = new_fitness

        # update the child's genome and fitness
        child.genome = best_genome
        child.fitness = best_fitness
        return child"""

a = Algorithm_Memetic(100, 40, 0.02, 30, 15, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300], "tournament", 8)
#a = Algorithm_Memetic(20, 30, 0.4, 60, 60, 15, [random.randint(2, 5) for _ in range(15)], [random.randint(100, 2500) for _ in range(15)])
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