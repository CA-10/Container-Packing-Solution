from Algorithms.GA.Member_Cartesian import Member_Cartesian
from Algorithms.Container_Context import Container_Context
import Algorithms.GA.crossover_functions as crossover_functions
from Algorithms.GA.Gene_Cartesian import Gene_Cartesian
import random

class Population_Cartesian:
    def __init__(self, population_size: int, container_context: Container_Context, radii: list[float], masses: list[int]):
        if len(radii) != len(masses):
            raise ValueError("radii and masses must be same length")
        
        self.population_size = population_size
        self.container_context = container_context
        self.radii = radii
        self.masses = masses
        self.num_circles = len(radii)
        self.fitnesses: list[float] = []

        self.population = [Member_Cartesian(radii, masses, container_context, self.num_circles) for _ in range(population_size)]

    def calculate_fitness(self) -> float:
        self.fitnesses = [] #Clear the fitnesses otherwise we end up with a growing fitness list

        for member in self.population:
            self.fitnesses.append(member.calculate_fitness())
        
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

    def crossover(self, parent_a: Member_Cartesian, parent_b: Member_Cartesian) -> tuple[Member_Cartesian, Member_Cartesian]:
        parent_a_positions = [parent_a.genome[i].position for i in range(len(parent_a.genome))]
        parent_b_positions = [parent_b.genome[i].position for i in range(len(parent_b.genome))]
        alpha = 0.05

        child1_positions, child2_positions = crossover_functions.blended_crossover(parent_a_positions, parent_b_positions, alpha)

        child1 = Member_Cartesian(self.radii, self.masses, self.container_context, self.num_circles)
        child2 = Member_Cartesian(self.radii, self.masses, self.container_context, self.num_circles)

        child1.genome = []
        child2.genome = []

        for i in range(len(child1_positions)):
            gene = Gene_Cartesian(child1_positions[i].x, child1_positions[i].y, parent_a.genome[i].radius, parent_a.genome[i].mass) #type: ignore
            child1.genome.append(gene)

        for i in range(len(child2_positions)):
            gene = Gene_Cartesian(child2_positions[i].x, child2_positions[i].y, parent_a.genome[i].radius, parent_a.genome[i].mass) #type: ignore
            child2.genome.append(gene)
        
        return child1, child2
    
    def mutate(self, mutation_rate):
        for member in self.population:
            member.mutate(mutation_rate)