from GA.Member_OrderBased import Member_OrderBased
from Container_Context import Container_Context
import GA.crossover_functions as crossover_functions
from GA.Gene_OrderBased import Gene_OrderBased
import random
import Operators.placement_functions as placement_functions
from Vector2 import Vector2

class Population_OrderBased:
    def __init__(self, population_size: int, container_context: Container_Context, radii: list[float], masses: list[int]):
        if len(radii) != len(masses):
            raise ValueError("radii and masses must be same length")
        
        self.population_size = population_size
        self.container_context = container_context
        self.radii = radii
        self.masses = masses
        self.num_circles = len(radii)
        self.fitnesses: list[float] = []

        self.population = [Member_OrderBased(radii, masses, container_context, self.num_circles) for _ in range(population_size)]

    def calculate_fitness(self) -> float:
        self.fitnesses = [] #Clear the fitnesses otherwise we end up with a growing fitness list

        for member in self.population:
            self.fitnesses.append(member.calculate_fitness())
        
        return max(self.fitnesses)
    
    def place_members(self) -> None:
        #Places the circles using the order in-place so that the next step can calculate fitness based on the x, y positions of the member circles.
        for member in self.population:
            radii_sorted = []
            masses_sorted = []
            orders = []

            for gene in member.genome:
                orders.append(gene.order)

            for order in orders:
                radii_sorted.append(member.radii[order])
                masses_sorted.append(member.masses[order])

            positions_and_r, masses = placement_functions.place_circles(radii_sorted, masses_sorted, self.container_context)

            for i, order in enumerate(orders):
                position = Vector2(positions_and_r[i][0], positions_and_r[i][1])
                radius = positions_and_r[i][2]
                mass = masses[i]

                #Update the member's genome in-place using the placed positions
                member.genome[order].position = position
                member.genome[order].radius = radius
                member.genome[order].mass = mass

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

    def crossover(self, parent_a: Member_OrderBased, parent_b: Member_OrderBased) -> tuple[Member_OrderBased, Member_OrderBased]:
        parent_a_orders = [parent_a.genome[i].order for i in range(len(parent_a.genome))]
        parent_b_orders = [parent_b.genome[i].order for i in range(len(parent_b.genome))]

        child1_orders, child2_orders = crossover_functions.ordered_crossover(parent_a_orders, parent_b_orders)

        child1 = Member_OrderBased(self.radii, self.masses, self.container_context, self.num_circles)
        child2 = Member_OrderBased(self.radii, self.masses, self.container_context, self.num_circles)

        child1.genome = []
        child2.genome = []

        for i in range(len(child1_orders)):
            gene = Gene_OrderBased(child1_orders[i], parent_a.genome[i].radius, parent_a.genome[i].mass) #type: ignore
            child1.genome.append(gene)

        for i in range(len(child2_orders)):
            gene = Gene_OrderBased(child2_orders[i], parent_a.genome[i].radius, parent_a.genome[i].mass) #type: ignore
            child2.genome.append(gene)
        
        return child1, child2
    
    def mutate(self, mutation_rate):
        for member in self.population:
            member.mutate(mutation_rate)