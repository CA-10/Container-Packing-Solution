from GA.Gene import Gene
import random
from Vector2 import Vector2

class Gene_Cartesian(Gene):
    def __init__(self, x: int, y: int, radius: float, mass: int):
        self.position = Vector2(x, y)

        #Phenotypes
        self.radius = radius
        self.mass = mass

    def mutate(self, mutation_rate: float) -> None:
        if random.random() < mutation_rate:
            new_x = self.position.x + random.randint(-20, 20)
            new_y = self.position.y + random.randint(-20, 20)

            self.position = Vector2(new_x, new_y)