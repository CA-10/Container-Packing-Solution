from abc import ABC as abstract, abstractmethod
from Container_Context import Container_Context

class Member(abstract):
    def __init__(self, radii: list[float], masses: list[int], container_context: Container_Context, num_genes: int):
        self.radii = radii
        self.masses = masses
        self.container_context = container_context
        self.num_genes = num_genes

    @abstractmethod
    def init_genome(self) -> None:
        pass

    @abstractmethod
    def calculate_fitness(self) -> float:
        pass

    @abstractmethod
    def mutate(self, mutation_rate: float) -> None:
        pass