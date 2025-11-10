import random
import math
from GA.Member import Member
from Operators.penalty_functions import *

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
        
    def crossover(self, parent_A, parent_B, alpha=0.5):
        """
        Perform a blended crossover (BLX-α) for genomes made of (x, y) tuples.
        Each coordinate is blended separately.
        """
        child1_genome = []
        child2_genome = []

        for (xA, yA), (xB, yB) in zip(parent_A.genome, parent_B.genome):
            # --- Blend X coordinate ---
            x_min, x_max = min(xA, xB), max(xA, xB)
            x_diff = x_max - x_min
            x_lower = x_min - alpha * x_diff
            x_upper = x_max + alpha * x_diff
            new_x1 = random.uniform(x_lower, x_upper)
            new_x2 = random.uniform(x_lower, x_upper)

            # --- Blend Y coordinate ---
            y_min, y_max = min(yA, yB), max(yA, yB)
            y_diff = y_max - y_min
            y_lower = y_min - alpha * y_diff
            y_upper = y_max + alpha * y_diff
            new_y1 = random.uniform(y_lower, y_upper)
            new_y2 = random.uniform(y_lower, y_upper)

            # Add blended genes as tuples
            child1_genome.append((new_x1, new_y1))
            child2_genome.append((new_x2, new_y2))

        # Create child Member objects
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
            penalty += calculate_overlap_penalty(member.genome, self.radii) * 1.3
            penalty += calculate_bounds_overlap_penalty(member.genome, self.radii, self.container_width, self.container_height) * 1.0
            penalty += calculate_com_penalty(member.genome, self.masses, [self.container_width / 2, self.container_height / 2])[1] * 1.0
            penalty += calculate_touching_penalty(member.genome, self.radii) * 1.0

            fitness = 1 / (1 + penalty)
            self.fitnesses.append(fitness)
        
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