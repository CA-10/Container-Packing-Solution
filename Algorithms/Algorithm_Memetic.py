from AlgorithmBase import AlgorithmBase as AB
from GA.Population import Population
from Visualisation.Custom_Visualisation import Custom_Visualisation #TODO REMOVE
from Visualisation.Visualisation_Object import Visualisation_Object #TODO REMOVE
import Visualisation.Results_Graphs as Results_Graphs #TODO REMOVE
import time
from Operators.penalty_functions import *

class Algorithm_Memetic(AB):

    def __init__(self, max_generations, population_size, mutation_rate, container_width, container_height, num_circles, radii, masses, selection_method="roulette", tournament_size=3):
        self.gen_count = 0
        self.max_generations = max_generations
        self.population_size = population_size
        self.container_width = container_width
        self.container_height = container_height
        self.radii = radii
        self.masses = masses
        self.best_fitnesses = []
        self.selection_method = selection_method
        self.tournament_size = tournament_size
        
        #Create the population object and assign to self.population
        self.population = Population(population_size, mutation_rate, container_width, container_height, num_circles, radii, masses)