import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def draw_fitness_over_gens(fitness_values, display=True, title="Fitness Over Generations", xlabel="Generation", ylabel="Fitness", linelabel="Best Fitness"):
    if not fitness_values:
        return None
    
    num_gens = len(fitness_values)
    gens = [i for i in range(num_gens)]
    
    fig = Figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    if num_gens > 1:
        ax.plot(gens, fitness_values, label=linelabel, linewidth=2)
    elif num_gens == 1:
        ax.scatter(1, gens[0])

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend()

    if display:
        plt.show()
    
    return fig