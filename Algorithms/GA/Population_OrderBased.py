from GA.Population import Population
from GA.Member_OrderBased import Member_OrderBased
from Operators.penalty_functions import *
from Operators.crossover import *
from Operators.mutation import *
from Operators.placement_funcs import *

class Population_OrderBased(Population):

    def __init__(self, population_size, mutation_rate, container_width, container_height, num_circles, radii, masses):
        super().__init__(population_size, mutation_rate, container_width, container_height, num_circles, radii, masses)
        self.mapping_dict = {}
        self.placed_circles = []
        self.placed_masses = []

        for i in range(self.num_circles):
            self.mapping_dict[chr(65 + i)] = (radii[i], masses[i])
        
    def init_population(self):
        for _ in range(self.population_size):
            self.population.append(Member_OrderBased(self.num_circles))
            
    def population_tostring(self):
        result = "["  

        for member in self.population:
            result += "[" + ", ".join(str(gene) for gene in member.genome) + "], "

        result += "]"
        
        return result
        
    def crossover(self, parent_A, parent_B, alpha=0.5):
        child1, child2 = ordered_crossover(parent_A, parent_B)

        child1_member = Member_OrderBased(self.num_circles)
        child1_member.genome = child1

        child2_member = Member_OrderBased(self.num_circles)
        child2_member.genome = child2

        return child1_member, child2_member
  
    def mutate(self, genome):
        new_genome = shuffle_mutation(genome, self.mutation_rate)
        return new_genome
    
    def calculate_fitness(self):
        self.fitnesses = []
        
        for member in self.population:
            ordered_radii = []
            ordered_masses = []

            for gene in member.genome:
                ordered_radii.append(self.mapping_dict[gene][0])
                ordered_masses.append(self.mapping_dict[gene][1])

            self.placed_circles, self.placed_masses = place_circles(ordered_radii, ordered_masses, self.container_width, self.container_height, order_based_on_com=False)

            positions = []
            radii = []

            for (x, y, r) in self.placed_circles:
                positions.append((x, y))
                radii.append(r)
                
            penalty = calculate_total_penalty(positions, radii, self.placed_masses, self.container_width, self.container_height)
            fitness = math.exp(-0.001 * penalty)

            self.fitnesses.append(fitness)

        return max(self.fitnesses)
    
    def evaluate_individual(self, genome):
        ordered_radii = []
        ordered_masses = []

        for gene in genome:
            ordered_radii.append(self.mapping_dict[gene][0])
            ordered_masses.append(self.mapping_dict[gene][1])

        placed_circles, placed_masses = place_circles(ordered_radii, ordered_masses, self.container_width, self.container_height, order_based_on_com=False)

        positions = []
        radii = []

        for (x, y, r) in placed_circles:
            positions.append((x, y))
            radii.append(r)
            
        penalty = calculate_total_penalty(positions, radii, placed_masses, self.container_width, self.container_height)
        fitness = math.exp(-0.001 * penalty)

        return fitness

    def roulette_wheel_selection(self):
        return super().roulette_wheel_selection()
    
    def tournament_selection(self, tournament_size=3):
        return super().tournament_selection(tournament_size)