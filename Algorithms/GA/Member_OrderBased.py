from Algorithms.GA.Member import Member
from Algorithms.GA.Gene_OrderBased import Gene_OrderBased
import random
import Algorithms.Operators.penalty_functions as penalty_functions
from Algorithms.Vector2 import Vector2
from Algorithms.Container_Context import Container_Context
import math

class Member_OrderBased(Member):
    def __init__(self, radii: list[float], masses: list[int], container_context: Container_Context, num_genes: int):
        super().__init__(radii, masses, container_context, num_genes)
        self.genome: list[Gene_OrderBased] = []

        self.init_genome()

    def init_genome(self) -> None:
        for i in range(self.num_genes):
            random_order = random.randint(0, self.num_genes - 1)

            self.genome.append(Gene_OrderBased(random_order, self.radii[i], self.masses[i]))
    
    def calculate_fitness(self) -> float:
        positions = [self.genome[i].position for i in range(len(self.genome))]
        radii = [self.genome[i].radius for i in range(len(self.genome))]
        masses = [self.genome[i].mass for i in range(len(self.genome))]

        p1 = penalty_functions.calculate_overlap_penalty(positions, radii)
        p2 = penalty_functions.calculate_bounds_overlap_penalty(positions, radii, self.container_context.container_width, self.container_context.container_height)
        p3 = penalty_functions.calculate_com_penalty(positions, masses, Vector2(self.container_context.container_width / 2, self.container_context.container_height / 2))[1]
        p4 = penalty_functions.calculate_packing_fitness(positions, radii)

        penalty = (15.0 * p1) + (10.0 * p2) + (5.0 * p3) + (1.6 * p4)
        #fitness = math.exp(-0.001 * penalty)
        fitness = -penalty

        return fitness
    
    def mutate(self, mutation_rate: float) -> None:
        for gene in self.genome:
            gene.mutate(mutation_rate)