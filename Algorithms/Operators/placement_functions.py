import math
import Operators.penalty_functions as penalty_functions
from Container_Context import Container_Context

def generate_candidate_positions(placed_circles, circle_r, container_width, container_height):
    candidate_positions = []

    #If haven't placed any circles yet, place the circle at the center of the container
    if not placed_circles:
        candidate_positions.append((container_width / 2, container_height / 2))
    else:
        #Generate candidate positions around existing circles
        for (x, y, r) in placed_circles:
            for angle in linspace(0, 2 * math.pi, 50):
                new_x = x + (circle_r + r) * math.cos(angle)
                new_y = y + (circle_r + r) * math.sin(angle)
                
                if (circle_r <= new_x <= container_width - circle_r and
                    circle_r <= new_y <= container_height - circle_r):
                    candidate_positions.append((new_x, new_y))
                        
    return candidate_positions

def calc_dist(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def linspace(start, stop, num):
    if num == 1:
        return [start]
    
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]

def does_overlap(placed_circles, circle_position, circle_r):
    for (x, y, r) in placed_circles:
        dx = circle_position[0] - x
        dy = circle_position[1] - y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist < (r + circle_r):
            return True
            
    return False

def calculate_potential_com(placed_circles, placed_masses, new_circle, m):
    com = [0, 0]
    sum_mx = 0
    sum_my = 0
    total_mass = sum(placed_masses) + m
    
    for i in range(len(placed_masses)):
        circle_x = placed_circles[i][0]
        circle_y = placed_circles[i][1]
        circle_mass = placed_masses[i]
        
        sum_mx += circle_x * circle_mass
        sum_my += circle_y * circle_mass
    
    sum_mx += new_circle[0] * m
    sum_my += new_circle[1] * m

    com[0] = sum_mx / total_mass
    com[1] = sum_my / total_mass
    
    return com

def place_circles(radii: list[float], masses: list[int], masks: list[int], container_context: Container_Context, remaining_mass: int, respect_mass_limit=True, order_based_on_com=True) -> tuple[list[tuple[float, float, float]], list[int], list[int]]:
    placed_circles = []
    placed_masses = []
    placed_masks = []

    for r, m in zip(radii, masses):
        if respect_mass_limit and m > remaining_mass:
            continue

        candidate_positions = generate_candidate_positions(placed_circles, r, container_context.container_width, container_context.container_height)
        valid_candidates = [p for p in candidate_positions if not does_overlap(placed_circles, p, r)]
        
        if not valid_candidates:
            print(f"No valid placement found for radius {r}")
            continue
        
        potential_com_distances = []
        
        if order_based_on_com:
            for candidate in valid_candidates:
                potential_com = calculate_potential_com(placed_circles, placed_masses, candidate, m)
                dist = calc_dist(potential_com, (container_context.container_width / 2, container_context.container_height / 2))
                potential_com_distances.append(dist)
            
            #Sort by COM distance
            sorted_by_com = sorted(zip(potential_com_distances, valid_candidates), key=lambda x: x[0])
            
            #Take top candidate by COM
            best_candidate = sorted_by_com[0][1]
        else:
            best_candidate = valid_candidates[0]
        
        #Store with radius and mask for later reference
        placed_circles.append((best_candidate[0], best_candidate[1], r))
        placed_masses.append(m)
        placed_masks.append(1)

        remaining_mass -= m

    #We've reached the end of placing all the circles, need to fill in the rest of the mask with 0
    while len(placed_masks) != len(masks):
        placed_masks.append(0)
    
    return placed_circles, placed_masses, placed_masks