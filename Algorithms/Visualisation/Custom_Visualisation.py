from matplotlib.figure import Figure
from Algorithms.Visualisation.Visualisation_Base import Visualisation_Base
from matplotlib.patches import Circle
import matplotlib.pyplot as plt

class Custom_Visualisation(Visualisation_Base):
    def visualise(self, visualisation_object, self_display=False, generation=None): #type: ignore

        #Use OO Figure instead of pyplot to avoid polluting global state
        fig = Figure(figsize=(13, 13))
        ax = fig.add_subplot(111)

        container = plt.Rectangle( #type: ignore
            (0, 0),
            visualisation_object.container_width,
            visualisation_object.container_height,
            fill=False,
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(container)

        for (x, y), r in zip(visualisation_object.circles, visualisation_object.radii):
            circle = Circle((x, y), r, fill=True, alpha=0.5, edgecolor='blue', facecolor='skyblue')
            ax.add_patch(circle)
            ax.plot(x, y, 'ro', markersize=3)

        com = visualisation_object.com
        ax.scatter(com[0], com[1], marker='x', color='red', s=100)

        ax.set_xlim(-5, visualisation_object.container_width + 5)
        ax.set_ylim(-5, visualisation_object.container_height + 5)
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(f"Best Member (Gen {generation if generation is not None else '?'})")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, linestyle='--', alpha=0.3)

        return fig, ax