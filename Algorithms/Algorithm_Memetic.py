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

class Algorithm_Memetic(AB):

    def __init__(self, max_generations, population_size, mutation_rate, container_width, container_height, num_circles, radii, masses, selection_method="roulette", tournament_size=3):
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
        self.num_circles = num_circles
        self.greedy_algorithm = None
        
        #Create the population object and assign to self.population
        self.population = Population_OrderBased(population_size, mutation_rate, container_width, container_height, num_circles, radii, masses)
    
    def run(self):
        start_time = time.time()
        
        for gen in range(self.max_generations):
            self.run_generation()  
            max_fitness = self.population.calculate_fitness()
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

        overall_fitness = self.population.calculate_fitness()

        self.fitness = overall_fitness
        
        self.print_stats()
            
    def run_generation(self, show_pop_output=False, elitism_count=1):
        #Evaluate current population
        self.population.calculate_fitness()

        #Keep elites
        fitnesses = self.population.fitnesses
        sorted_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)
        elites = [self.population.population[i] for i in sorted_indices[:elitism_count]]

        temp_population = elites.copy()

        while len(temp_population) < self.population_size:
            if self.selection_method == "roulette":
                parent_a = self.population.roulette_wheel_selection()
                parent_b = self.population.roulette_wheel_selection()
            elif self.selection_method == "tournament":
                parent_a = self.population.tournament_selection(self.tournament_size)
                parent_b = self.population.tournament_selection(self.tournament_size)
            else:
                raise Exception(f"{self.selection_method} not a valid selection method")

            child1, child2 = self.population.crossover(parent_a.genome, parent_b.genome)

            #Mutate and locally improve each child
            for child in (child1, child2):
                child.genome = self.population.mutate(child.genome)
                child = self.local_search(child)  #Local Search
                temp_population.append(child)

                if len(temp_population) >= self.population_size:
                    break

        #Replace old population
        self.population.population = temp_population[:self.population_size]

    def local_search(self, child, max_attempts=15):
        best_genome = child.genome[:]
        best_fitness = self.population.evaluate_individual(child.genome)

        for _ in range(max_attempts):
            # create a neighbor by swapping two positions
            i, j = random.sample(range(len(best_genome)), 2)
            new_genome = best_genome[:]
            new_genome[i], new_genome[j] = new_genome[j], new_genome[i]

            new_fitness = self.population.evaluate_individual(new_genome)

            if new_fitness > best_fitness:
                best_genome = new_genome
                best_fitness = new_fitness

        # update the child's genome and fitness
        child.genome = best_genome
        child.fitness = best_fitness
        return child

a = Algorithm_Memetic(100, 5, 0.3, 30, 15, 14, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300], "tournament")
#a = Algorithm_Memetic(100, 50, 0.8, 50, 50, 15, [random.randint(2, 10) for _ in range(15)], [random.randint(100, 2500) for _ in range(15)])
a.run()

pos = []
radii_ordered = []
masses_ordered = []

for circle in a.population.placed_circles:
    pos.append((circle[0], circle[1]))  # x, y position
    radii_ordered.append(circle[2])      # radius stored in the tuple

# Get masses in the same order they were placed
masses_ordered = a.population.placed_masses

com = calculate_com_penalty(pos, masses_ordered, radii_ordered)[0]
cb = Visualisation_Object(pos, radii_ordered, masses_ordered, com, 
                          a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)