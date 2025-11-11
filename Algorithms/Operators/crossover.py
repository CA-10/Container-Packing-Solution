import random

def blended_crossover(parent_a_positions, parent_b_positions, alpha):
    """
    Perform a blended crossover (BLX-α) for genomes made of (x, y) tuples.
    Each coordinate is blended separately.
    """
    child1_positions = []
    child2_positions = []

    for (xA, yA), (xB, yB) in zip(parent_a_positions, parent_b_positions):
        #--- Blend X coordinate ---
        x_min, x_max = min(xA, xB), max(xA, xB)
        x_diff = x_max - x_min
        x_lower = x_min - alpha * x_diff
        x_upper = x_max + alpha * x_diff
        new_x1 = random.uniform(x_lower, x_upper)
        new_x2 = random.uniform(x_lower, x_upper)

        #--- Blend Y coordinate ---
        y_min, y_max = min(yA, yB), max(yA, yB)
        y_diff = y_max - y_min
        y_lower = y_min - alpha * y_diff
        y_upper = y_max + alpha * y_diff
        new_y1 = random.uniform(y_lower, y_upper)
        new_y2 = random.uniform(y_lower, y_upper)

        #Add blended genes as tuples
        child1_positions.append((new_x1, new_y1))
        child2_positions.append((new_x2, new_y2))

    return child1_positions, child2_positions

def ordered_crossover(parent_a, parent_b):
    n = len(parent_a)
    
    p1, p2 = sorted(random.sample(range(n), 2))
    
    child1 = [None for _ in range(n)]
    child2 = [None for _ in range(n)]

    child1[p1:p2+1] = parent_a[p1:p2+1]
    child2[p1:p2+1] = parent_b[p1:p2+1]

    fill_from_parent(child1, parent_b, p2)
    fill_from_parent(child2, parent_a, p2)

    return child1, child2   

def fill_from_parent(child, donor_parent, start_index):
    n = len(child)
    current_index = (start_index + 1) % n
    
    for gene in donor_parent:
        if gene not in child:
            child[current_index] = gene
            current_index = (current_index + 1) % n