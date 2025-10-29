from AlgorithmBase import AlgorithmBase as AB
from GA.Population import Population
import random
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import time

class Algorithm_GA(AB):
    
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
        
        #Create the population object and assign to self.population
        self.population = Population(population_size, mutation_rate, container_width, container_height, num_circles, radii, masses)
    
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
        self.fitness = self.population.calculate_fitness()
        
        self.print_stats()
            
    def run_generation(self, show_pop_output=False):
        self.population.calculate_fitness()
        
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

            for child in (child1, child2):
                child_com = child.calculate_com_penalty(self.masses, [a.container_width / 2, a.container_height / 2])[0]
                child.genome = self.population.mutate(child.genome)
                temp_population.append(child)

            temp_population = temp_population[:self.population_size]

        self.population.population = temp_population

        #Print out the new population if the flag is enabled
        if show_pop_output:
            print(self.population.population_tostring())
            
#====TODO Remove, this is just testing code.====
a = Algorithm_GA(300, 600, 0.03, 20, 15, 10, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500], "tournament", 5)
#a = Algorithm_GA(300, 700, 0.03, 100, 100, 10, [random.randint(3.0, 10.0) for _ in range(10)], [random.randint(100, 2500) for _ in range(10)])



a.run()


best_member = a.population.population[a.population.fitnesses.index(max(a.population.fitnesses))]

com = best_member.calculate_com_penalty(a.masses, [a.container_width / 2, a.container_height / 2])[0]
cb = Visualisation_Object(best_member.genome, a.radii, a.masses, com, a.container_width, a.container_height)

c = Custom_Visualisation()
c.visualise(cb)

Results_Graphs.draw_fitness_over_gens(a.best_fitnesses)