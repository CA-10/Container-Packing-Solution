import random
import math

class Member:
    
    def __init__(self, container_width, container_height, num_genes):
        self.genome = []
        self.container_width = container_width
        self.container_height = container_height
        
        #Randomly generate the Genome upon construction
        self.genome = [(random.randint(0, container_width), random.randint(0, container_height)) for _ in range(num_genes)]
    
    def calculate_overlap(self, radii):
        penalty = 0
    
        #For each circle, loop over each circle again apart from current and calculate overlap between all circles.
        for i in range(len(self.genome)):
            for j in range(i + 1, len(self.genome)):
                #Use the Euclidian distance formuala: d = sqrt((xi - xj)^2 + (yi - yj)^2)
                dx = self.genome[i][0] - self.genome[j][0]
                dy = self.genome[i][1] - self.genome[j][1]
                dist = math.sqrt(dx**2 + dy**2)
                
                #d >= ri + rj
                overlap = radii[i] + radii[j] - dist
                
                if overlap > 0:
                    penalty += overlap ** 2 #Add a squared penalty as we want to HEAVILY discourage overlapping.
        
        return penalty
    
    #TODO TEST!
    def calculate_bounds_overlap(self, radii):
        penalty = 0
        
        #For each circle, check if the circle is outside the bounds of the container
        for i in range(len(self.genome)):
            x, y = self.genome[i]
            r = radii[i]
            
            #Calculate the distance between the center and the container points and add penalty based on distance
            if x - r < 0:
                penalty += abs(x - r)
            
            if x + r > self.container_width:
                penalty += abs(x + r - self.container_width)
            
            if y - r < 0:
                penalty += abs(y - r)
                
            if y + r > self.container_height:
                penalty += abs(y + r - self.container_height)
        
        return penalty
        