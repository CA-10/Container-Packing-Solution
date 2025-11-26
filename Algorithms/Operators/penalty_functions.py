import math
from Algorithms.Vector2 import Vector2

def calculate_overlap_penalty(positions: list[Vector2], radii: list[float]) -> float:
    penalty = 0

    #For each circle, loop over each circle again apart from current and calculate overlap between all circles.
    for i in range(len(positions)):

        for j in range(i + 1, len(positions)):

            #Use the Euclidian distance formuala: d = sqrt((xi - xj)^2 + (yi - yj)^2)
            dx = positions[i].x - positions[j].x
            dy = positions[i].y - positions[j].y
            dist = math.sqrt(dx**2 + dy**2)
            
            #d >= ri + rj
            overlap = radii[i] + radii[j] - dist
            
            if overlap > 0:
                penalty += overlap ** 2 #Add a squared penalty as we want to HEAVILY discourage overlapping.
    
    return penalty

def calculate_com_penalty(positions: list[Vector2], masses: list[int], safety_zone_center: Vector2) -> tuple[Vector2, float]:
    penalty = 0
    com = Vector2(0, 0)
    sum_mx = 0
    sum_my = 0
    total_mass = sum(masses)

    for i in range(len(positions)):

        circle = positions[i]
        circle_x = circle.x
        circle_y = circle.y
        circle_mass = masses[i]
        
        sum_mx += circle_x * circle_mass
        sum_my += circle_y * circle_mass
    
    if total_mass != 0:
        com.x = sum_mx / total_mass
        com.y = sum_my / total_mass
    else:
        com.x = 0
        com.y = 0
    
    dist_from_center = math.sqrt((com.x - safety_zone_center.x)**2 + (com.y - safety_zone_center.y)**2)
    
    if dist_from_center > 0:
        penalty += dist_from_center
    
    return com, penalty

def calculate_packing_fitness(positions: list[Vector2], radii: list[float]) -> float:
    total_area = sum(r ** 2 for r in radii)

    if total_area == 0:
        return 1e6
    
    cx = sum(pos.x * r ** 2 for (pos), r in zip(positions, radii)) / total_area
    cy = sum(pos.y * r ** 2 for (pos), r in zip(positions, radii)) / total_area

    #Average squared distance from centroid (spread)
    spread_penalty = sum(((pos.x - cx) ** 2 + (pos.y - cy) ** 2) for (pos) in positions) / len(positions)
    
    return spread_penalty

def calculate_bounds_overlap_penalty(positions: list[Vector2], radii: list[float], container_width: int, container_height: int) -> float:
    penalty = 0
    
    #For each circle, check if the circle is outside the bounds of the container
    for i in range(len(positions)):

        x, y = positions[i].x, positions[i].y
        r = radii[i]
        
        #Calculate the distance between the center and the container points and add penalty based on distance
        if x - r < 0:
            penalty += abs(x - r)
        
        if x + r > container_width:
            penalty += abs(x + r - container_width)
        
        if y - r < 0:
            penalty += abs(y - r)
            
        if y + r > container_height:
            penalty += abs(y + r - container_height)
    
    return penalty