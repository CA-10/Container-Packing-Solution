import random

def cartesian_mutation(genome, mutation_rate):
    new_genome = []
    
    for gene in genome:
        probability = random.random()
        
        if probability < mutation_rate:
            new_x = gene[0] + random.randint(-20, 20)
            new_y = gene[1] + random.randint(-20, 20)
            
            new_genome.append((new_x, new_y))
        else:
            new_genome.append(gene)
    
    return new_genome

def swap_mutation(genome, mutation_rate):
    probability = random.random()

    if probability < mutation_rate:
        point1 = random.randint(len(genome) - 1)
        point2 = random.randint(len(genome) - 1)

        genome[point1], genome[point2] = genome[point2], genome[point1]
    
    return genome