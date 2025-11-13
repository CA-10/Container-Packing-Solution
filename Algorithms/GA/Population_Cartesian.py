from GA.Population import Population
from GA.Member_Cartesian import Member_Cartesian
from Operators.penalty_functions import *
from Operators.crossover import *
from Operators.mutation import *

class Population_Cartesian(Population):

    def __init__(self, population_size, mutation_rate, container_width, container_height, num_circles, radii, masses):
        super().__init__(population_size, mutation_rate, container_width, container_height, num_circles, radii, masses)
    
    def init_population(self):
        for _ in range(self.population_size):
            self.population.append(Member_Cartesian(self.container_width, self.container_height, self.num_circles))
            
    def population_tostring(self):
        result = "["  

        for member in self.population:
            result += "[" + ", ".join(str(gene) for gene in member.genome) + "], "

        result += "]"
        
        return result
        
    def crossover(self, parent_A, parent_B, alpha=0.5):
        child1, child2 = blended_crossover(parent_A, parent_B, alpha)

        child1_member = Member_Cartesian(self.container_width, self.container_height, self.num_circles)
        child1_member.genome = child1

        child2_member = Member_Cartesian(self.container_width, self.container_height, self.num_circles)
        child2_member.genome = child2

        return child1_member, child2_member
  
    def mutate(self, genome):
        new_genome = cartesian_mutation(genome, self.mutation_rate)
        return new_genome
    
    def calculate_fitness(self):
        self.fitnesses = []
        
        for member in self.population:
            penalty = calculate_total_penalty(member.genome, self.radii, self.masses, self.container_width, self.container_height)

            fitness = math.exp(-0.001 * penalty)
            self.fitnesses.append(fitness)
        
        return max(self.fitnesses)
        
    def roulette_wheel_selection(self):
        return super().roulette_wheel_selection()
    
    def tournament_selection(self, tournament_size=3):
        return super().tournament_selection(tournament_size)