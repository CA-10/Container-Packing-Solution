import random
from abc import ABC, abstractmethod

class Member(ABC):
    
    def __init__(self, num_genes):
        self.num_genes = num_genes
        
        self.init_genome()

    @abstractmethod
    def init_genome(self):
        pass