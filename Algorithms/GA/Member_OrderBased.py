import random
from GA.Member import Member

class Member_OrderBased(Member):
    
    def __init__(self, num_genes):
        super().__init__(num_genes)
    
    def init_genome(self):
        #Randomly generate the Cartesian coordinates upon construction
        self.genome = [chr(65 + i) for i in range(self.num_genes)]
        random.shuffle(self.genome)