from matplotlib.figure import Figure
from Algorithms.Visualisation.Visualisation_Base import Visualisation_Base
from matplotlib.patches import Circle
import matplotlib.pyplot as plt

class Custom_Visualisation(Visualisation_Base):
    def visualise(self, visualisation_object, self_display=False, generation=None): #type: ignore

        #Use OO Figure instead of pyplot to avoid polluting global state
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111)

        container = plt.Rectangle( #type: ignore
            (0, 0),
            visualisation_object.container_width,
            visualisation_object.container_height,
            fill=False,
            edgecolor='black',
            linewidth=2
        )

        centre = (visualisation_object.container_width / 2, visualisation_object.container_height / 2)

        safety_zone_width = 0.6 * visualisation_object.container_width
        safety_zone_height = 0.6 * visualisation_object.container_height

        safety_zone = plt.Rectangle( #type: ignore
            (centre[0] - safety_zone_width / 2, centre[1] - safety_zone_height / 2),  # bottom-left corner
            safety_zone_width,
            safety_zone_height,
            fill=True,
            color=(0.43, 1, 0.49, 0.3),
            edgecolor='green',
            linewidth=2,
            linestyle='--'
        )

        ax.add_patch(container)
        ax.add_patch(safety_zone)

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