import math

def calculate_overlap_penalty(positions, radii):
    penalty = 0

    #For each circle, loop over each circle again apart from current and calculate overlap between all circles.
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            #Use the Euclidian distance formuala: d = sqrt((xi - xj)^2 + (yi - yj)^2)
            dx = positions[i][0] - positions[j][0]
            dy = positions[i][1] - positions[j][1]
            dist = math.sqrt(dx**2 + dy**2)
            
            #d >= ri + rj
            overlap = radii[i] + radii[j] - dist
            
            if overlap > 0:
                penalty += overlap ** 2 #Add a squared penalty as we want to HEAVILY discourage overlapping.
    
    return penalty
    
def calculate_touching_penalty(positions, radii, desired_distance_factor=2.4):
    #Penalize circles which are not touching their neighbours. This will help reduce wasted space.
    penalty = 0
    
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dx = positions[i][0] - positions[j][0]
            dy = positions[i][1] - positions[j][1]
            dist = math.sqrt(dx**2 + dy**2)
            
            desired_distance = (radii[i] + radii[j]) * desired_distance_factor
            
            #Only penalize if circles are too far apart (don't interfere with overlaps)
            if dist > desired_distance:
                penalty += (dist - desired_distance) ** 2
                
    return penalty

def calculate_bounds_overlap_penalty(positions, radii, container_width, container_height):
    penalty = 0
    
    #For each circle, check if the circle is outside the bounds of the container
    for i in range(len(positions)):
        x, y = positions[i]
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
    
def calculate_com_penalty(positions, masses, safety_zone_center):
    penalty = 0
    com = [0, 0]
    sum_mx = 0
    sum_my = 0
    total_mass = sum(masses)
    
    for i in range(len(positions)):
        circle = positions[i]
        circle_x = circle[0]
        circle_y = circle[1]
        circle_mass = masses[i]
        
        sum_mx += circle_x * circle_mass
        sum_my += circle_y * circle_mass
    
    com[0] = sum_mx / total_mass
    com[1] = sum_my / total_mass
    
    dist_from_center = math.sqrt((com[0] - safety_zone_center[0])**2 + (com[1] - safety_zone_center[1])**2)
    
    if dist_from_center > 0:
        penalty += dist_from_center ** 2
    
    return com, penalty