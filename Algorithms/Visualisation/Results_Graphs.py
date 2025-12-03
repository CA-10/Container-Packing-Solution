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

def draw_comparison_bars(case_names, values_algorithms, title="Fitness Comparison", xlabel="Algorithms", ylabel="abs(Fitness)"):
    algorithms = list(values_algorithms[0].keys())
    n_algorithms = len(algorithms)
    n_cases = len(case_names)

    x_positions = list(range(n_algorithms))
    total_group_width = 0.8
    bar_width = total_group_width / n_cases

    colors = plt.get_cmap("Paired").colors  #type: ignore

    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    for case_idx, case_name in enumerate(case_names):
        values = [abs(values_algorithms[case_idx][alg]) for alg in algorithms]

        bar_positions = [x + case_idx * bar_width for x in x_positions]

        ax.bar(bar_positions, values, bar_width, 
               label=case_name, 
               color=colors[case_idx % len(colors)])

    tick_positions = [x + (total_group_width - bar_width) / 2 for x in x_positions]
    ax.set_xticks(tick_positions, algorithms)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    fig.tight_layout()

    return fig