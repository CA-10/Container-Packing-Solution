import matplotlib.pyplot as plt

class HistoryRecord:
    def __init__(self, console, visualisation_fig, fitness_history):
        self.console_history:str = console
        self.visualisation_history = visualisation_fig
        self.fitness_history = fitness_history