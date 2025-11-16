import random
from Vector2 import Vector2

def blended_crossover(parent_a_positions: list[Vector2], parent_b_positions: list[Vector2], alpha: float) -> tuple[list[Vector2], list[Vector2]]:
    """
    Perform a blended crossover (BLX-α) for genomes made of (x, y) tuples.
    Each coordinate is blended separately.
    """
    child1_positions = []
    child2_positions = []

    for vec_a, vec_b in zip((parent_a_positions), parent_b_positions):
        xA, xB = vec_a.x, vec_b.x
        yA, yB = vec_a.y, vec_b.y

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
        child1_positions.append(Vector2(new_x1, new_y1))
        child2_positions.append(Vector2(new_x2, new_y2))

    return child1_positions, child2_positions

def single_point_crossover(parent1_bits: list[int], parent2_bits: list[int]) -> tuple[list[int], list[int]]:

    if len(parent1_bits) != len(parent2_bits):
        raise ValueError("Parents must be the same length")

    point = random.randint(1, len(parent1_bits) - 1)

    child1 = parent1_bits[:point] + parent2_bits[point:]
    child2 = parent2_bits[:point] + parent1_bits[point:]

    return child1, child2