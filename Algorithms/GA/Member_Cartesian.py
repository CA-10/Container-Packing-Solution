import random
from GA.Member import Member

class Member_Cartesian(Member):
    
    def __init__(self, container_width, container_height, num_genes):
        super().__init__(container_width, container_height, num_genes)
    
    def init_genome(self):
        #Randomly generate the Cartesian coordinates upon construction
        self.genome = [(random.randint(0, self.container_width), random.randint(0, self.container_height)) for _ in range(self.num_genes)]