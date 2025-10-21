import random
from Member import Member

class GA:

    def __init__(self, population_size, mutation_rate, container_width, container_height, num_circles):
        self.population = []
        self.fitnesses = []
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.container_width = container_width
        self.container_height = container_height
        self.num_circles = num_circles
        self.gen = 0
    
    def init_population(self):
        for _ in range(self.population_size):
            self.population.append(Member(self.container_width, self.container_height, self.num_circles))
            
    def population_tostring(self):
        result = "["  

        for member in self.population:
            result += "[" + ", ".join(str(gene) for gene in member.genome) + "], "

        result += "]"
        
        return result
    
    def crossover(self, parent_A, parent_B):
        random_point = random.randint(1, len(parent_A.genome) - 1)
        
        child1 = parent_A.genome[:random_point] + parent_B.genome[random_point:]
        child2 = parent_B.genome[:random_point] + parent_A.genome[random_point:]
        
        return child1, child2
    
    def mutate(self, member):
        new_genome = []
        
        for gene in member.genome:
            probability = random.random()
            
            if probability < self.mutation_rate:
                #TODO: More complex genome mutations, possibly using COM aware methods.  
                new_x = gene[0] + random.randint(-20, 20)
                new_y = gene[1] + random.randint(-20, 20)
                
                new_genome.append((new_x, new_y))
            else:
                new_genome.append(gene)
        
        return new_genome
    
    def calculate_fitness(self):
        pass #TODO
    
    #This implements roulette wheel selection.
    def select(self):
        total_fitness = sum(self.fitnesses)
        
        if total_fitness == 0:
            return random.choice(self.population) #If all fitnesses are zero, pick randomly to avoid a crash.

        pick = random.uniform(0, total_fitness)
        current = 0
        
        for individual, fitness in zip(self.population, self.fitnesses):
            current += fitness
            if current >= pick:
                return individual