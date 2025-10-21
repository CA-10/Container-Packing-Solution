import random

class Member:
    
    def __init__(self, container_width, container_height, num_genes):
        self.genome = []
        
        #Randomly generate the Genome upon construction
        self.genome = [(random.randint(0, container_width), random.randint(0, container_height)) for _ in range(num_genes)]