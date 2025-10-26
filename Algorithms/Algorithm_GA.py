from AlgorithmBase import AlgorithmBase as AB
from GA.Population import Population
import random
from Visualisation.Custom_Visualisation import Custom_Visualisation
from Visualisation.Visualisation_Object import Visualisation_Object
import time

class Algorithm_GA(AB):
    
    def __init__(self, max_generations, population_size, mutation_rate, container_width, container_height, num_circles, radii, masses):
        self.gen_count = 0
        self.max_generations = max_generations
        self.population_size = population_size
        self.container_width = container_width
        self.container_height = container_height
        self.radii = radii
        self.masses = masses
        
        #Create the population object and assign to self.population
        self.population = Population(population_size, mutation_rate, container_width, container_height, num_circles, radii, masses)
    
    def run(self):
        start_time = time.time()
        
        for gen in range(self.max_generations):
            self.run_generation()  
            max_fitness = self.population.calculate_fitness()
            
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
            
    def run_generation(self, show_pop_output=False):
        self.population.calculate_fitness()
        
        temp_population = []
        
        for _ in range(self.population_size):
            parent_a = self.population.select()
            parent_b = self.population.select()
            
            child = self.population.crossover(parent_a, parent_b)
            child_com = child.calculate_com_penalty(self.masses, [a.container_width / 2, a.container_height / 2])[0]
            child.genome = self.population.mutate(child.genome)
            
            temp_population.append(child)
        
        self.population.population = temp_population

        #Print out the new population if the flag is enabled
        if show_pop_output:
            print(self.population.population_tostring())
            
#====TODO Remove, this is just testing code.====
a = Algorithm_GA(1000, 700, 0.06, 20, 15, 5, [2.0, 2.0, 1.5, 1.5, 1.2], [2500, 2500, 800, 800, 300])

a.run()


best_member = a.population.population[a.population.fitnesses.index(max(a.population.fitnesses))]

com = best_member.calculate_com_penalty(a.masses, [a.container_width / 2, a.container_height / 2])[0]
cb = Visualisation_Object(best_member.genome, a.radii, a.masses, com, a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)