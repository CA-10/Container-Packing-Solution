from Algorithms.GA.Gene import Gene
import random
from Algorithms.Vector2 import Vector2

class Gene_OrderBased(Gene):
    def __init__(self, order: int, radius: float, mass: int):
        self.order = order

        #Phenotypes
        self.radius = radius
        self.mass = mass
        self.position = Vector2(0, 0)

    def mutate(self, mutation_rate: float) -> None:
        if random.random() < mutation_rate:
            self.order = not self.order