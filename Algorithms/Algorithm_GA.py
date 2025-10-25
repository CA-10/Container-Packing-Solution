from AlgorithmBase import AlgorithmBase as AB
from GA.Population import Population
import random
from Visualisation.Custom_Visualisation import Custom_Visualisation

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
        for gen in range(self.max_generations):
            self.run_generation()  
            max_fitness = self.population.calculate_fitness()
            
            print(f"Generation: {gen}")
            print(f"Best Fitness: {max_fitness}")
            print(f"Average Fitness: {sum(self.population.normalised_fitnesses) / len(self.population.normalised_fitnesses)}")
            
            self.gen_count += 1
            self.num_iterations_or_generations += 1
            
            #Found a perfect solution, stop early
            if max_fitness == 1.0:
                break
            
    def run_generation(self, show_pop_output=False):
        self.population.calculate_fitness()
        
        temp_population = []
        
        for _ in range(self.population_size):
            parent_a = self.population.select()
            parent_b = self.population.select()
            
            child = self.population.crossover(parent_a, parent_b)
            child.genome = self.population.mutate(child.genome)
            
            temp_population.append(child)
        
        self.population.population = temp_population

        #Print out the new population if the flag is enabled
        if show_pop_output:
            print(self.population.population_tostring())
            
#====TODO Remove, this is just testing code.====
a = Algorithm_GA(2000, 200, 0.01, 100, 100, 20, [random.randint(2, 10) for _ in range(20)], [30, 40, 50])

a.run()

c = Custom_Visualisation()
c.visualise_best_member(a.population)