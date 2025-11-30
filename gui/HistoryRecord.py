import matplotlib.pyplot as plt

class HistoryRecord:
    def __init__(self, console, visualisation_fig):
        self.console_history:str = console
        self.visualisation_history = visualisation_fig