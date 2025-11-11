import random
import math
from GA.Member import Member
from Operators.penalty_functions import *
from Operators.crossover import *
from Operators.mutation import *

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
        child1, child2 = blended_crossover(parent_A, parent_B, alpha)

        child1_member = Member(self.container_width, self.container_height, self.num_circles)
        child1_member.genome = child1

        child2_member = Member(self.container_width, self.container_height, self.num_circles)
        child2_member.genome = child2

        return child1_member, child2_member
  
    def mutate(self, genome):
        new_genome = cartesian_mutation(genome, self.mutation_rate)
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