import random
import math
from GA.Member import Member

class Population:

    def __init__(self, population_size, mutation_rate, container_width, container_height, num_circles, radii, masses):
        self.population = []
        self.fitnesses = []
        self.radii = radii
        self.masses = masses
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.container_width = container_width
        self.container_height = container_height
        self.num_circles = num_circles
        
        self.init_population()
    
    def init_population(self):
        for _ in range(self.population_size):
            self.population.append(Member(self.container_width, self.container_height, self.num_circles))
            
    def population_tostring(self):
        result = "["  

        for member in self.population:
            result += "[" + ", ".join(str(gene) for gene in member.genome) + "], "

        result += "]"
        
        return result
    
    def crossover(self, parent_A, parent_B):
        #Choose a random crossover point (not at the ends)
        random_point = random.randint(1, len(parent_A.genome) - 1)

        #Create child genomes by swapping tails
        child1_genome = parent_A.genome[:random_point] + parent_B.genome[random_point:]
        child2_genome = parent_B.genome[:random_point] + parent_A.genome[random_point:]

        #Create child Member objects
        child1 = Member(self.container_width, self.container_height, self.num_circles)
        child2 = Member(self.container_width, self.container_height, self.num_circles)

        child1.genome = child1_genome
        child2.genome = child2_genome

        return child1, child2
  
    def mutate(self, genome):
        new_genome = []
        
        for gene in genome:
            probability = random.random()
            
            if probability < self.mutation_rate:
                #TODO: More complex genome mutations, possibly using COM aware methods.  
                new_x = gene[0] + random.randint(-20, 20)
                new_y = gene[1] + random.randint(-20, 20)
                
                new_genome.append((new_x, new_y))
            else:
                new_genome.append(gene)
        
        return new_genome
    
    def calculate_fitness(self):
        self.fitnesses = []
        
        for member in self.population:
            penalty = 0
            penalty += member.calculate_overlap(self.radii) * 3.0
            penalty += member.calculate_bounds_overlap(self.radii) * 1.0
            penalty += member.calculate_com_penalty(self.masses, [self.container_width / 2, self.container_height / 2])[1] * 1.0
            penalty += member.calculate_boundary_waste(self.radii) * 0.6

            fitness = 1 / (1 + penalty)
            self.fitnesses.append(fitness)
            #TODO: Need to incorporate COM, container bounds, wasted space.
        
        min_fitness = min(self.fitnesses)
        max_fitness = max(self.fitnesses)

        #Return the maximum normalised fitness
        return max(self.fitnesses)
    
    def roulette_wheel_selection(self):
        total_fitness = sum(self.fitnesses)
        
        if total_fitness == 0:
            return random.choice(self.population) #If all fitnesses are zero, pick randomly to avoid a crash.

        pick = random.uniform(0, total_fitness)
        current = 0
        
        for individual, fitness in zip(self.population, self.fitnesses):
            current += fitness
            if current >= pick:
                return individual
        
        return self.population[self.fitnesses.index(max(self.fitnesses))]
    
    def tournament_selection(self, tournament_size=3):
        participants = random.sample(list(zip(self.population, self.fitnesses)), tournament_size)
        winner = max(participants, key=lambda x: x[1])
        
        return winner[0]