"""
This is a data class which holds the data for the rendering code.
"""

class Visualisation_Object:
    
    def __init__(self, circles, radii, masses, com, container_width, container_height):
        self.circles = circles
        self.radii = radii
        self.masses = masses
        self.com = com
        self.container_width = container_width
        self.container_height = container_height