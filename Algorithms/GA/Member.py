import random
import math

class Member:
    
    def __init__(self, container_width, container_height, num_genes):
        self.container_width = container_width
        self.container_height = container_height
        
        #Randomly generate the Genome upon construction
        self.genome = [(random.randint(0, container_width), random.randint(0, container_height)) for _ in range(num_genes)]