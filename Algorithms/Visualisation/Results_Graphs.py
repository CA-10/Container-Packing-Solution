import matplotlib.pyplot as plt

def draw_fitness_over_gens(fitness_values, title="Fitness Over Generations", xlabel="Generation", ylabel="Fitness", linelabel="Best Fitness"):
    num_gens = len(fitness_values)
    gens = [i for i in range(num_gens)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(gens, fitness_values, label=linelabel, linewidth=2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()