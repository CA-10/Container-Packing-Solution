import random
from abc import ABC, abstractmethod

class Member(ABC):
    
    def __init__(self, container_width, container_height, num_genes):
        self.container_width = container_width
        self.container_height = container_height
        self.num_genes = num_genes
        
        self.init_genome()

    @abstractmethod
    def init_genome(self):
        pass