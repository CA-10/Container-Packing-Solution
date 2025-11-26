from GA.Member import Member
from GA.Gene_Cartesian import Gene_Cartesian
import random
import Operators.penalty_functions as penalty_functions
from Vector2 import Vector2
from Container_Context import Container_Context
import math

class Member_Cartesian(Member):
    def __init__(self, radii: list[float], masses: list[int], container_context: Container_Context, num_genes: int):
        super().__init__(radii, masses, container_context, num_genes)
        self.genome: list[Gene_Cartesian] = []

        self.init_genome()

    def init_genome(self) -> None:
        for i in range(self.num_genes):
            random_x = random.randint(0, self.container_context.container_width)
            random_y = random.randint(0, self.container_context.container_height)

            self.genome.append(Gene_Cartesian(random_x, random_y, self.radii[i], self.masses[i]))
    
    def calculate_fitness(self) -> float:
        positions = [self.genome[i].position for i in range(len(self.genome))]
        radii = [self.genome[i].radius for i in range(len(self.genome))]
        masses = [self.genome[i].mass for i in range(len(self.genome))]

        p1 = penalty_functions.calculate_overlap_penalty(positions, radii)
        p2 = penalty_functions.calculate_bounds_overlap_penalty(positions, radii, self.container_context.container_width, self.container_context.container_height)
        p3 = penalty_functions.calculate_com_penalty(positions, masses, Vector2(self.container_context.container_width / 2, self.container_context.container_height / 2))[1]
        p4 = penalty_functions.calculate_packing_fitness(positions, radii)

        penalty = (15.0 * p1) + (10.0 * p2) + (0.5 * p3) + (1.6 * p4)
        #fitness = math.exp(-0.001 * penalty)
        fitness = -penalty

        return fitness
    
    def mutate(self, mutation_rate: float) -> None:
        for gene in self.genome:
            gene.mutate(mutation_rate)