from abc import ABC as abstract, abstractmethod

class Gene(abstract):

    @abstractmethod
    def mutate(self, mutation_rate: float) -> None:
        pass