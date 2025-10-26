from Visualisation.Visualisation_Base import Visualisation_Base
from matplotlib.patches import Circle
import matplotlib.pyplot as plt

class Custom_Visualisation(Visualisation_Base):
    
    def visualise(self, visualisation_object, generation=None):
        fig, ax = plt.subplots(figsize=(8, 8))
        
        #Draw container boundary
        container = plt.Rectangle((0, 0), visualisation_object.container_width, visualisation_object.container_height,
                                  fill=False, edgecolor='black', linewidth=2)
        ax.add_patch(container)

        #Draw circles
        for (x, y), r in zip(visualisation_object.circles, visualisation_object.radii):
            circle = Circle((x, y), r, fill=True, alpha=0.5, edgecolor='blue', facecolor='skyblue')
            ax.add_patch(circle)
            ax.plot(x, y, 'ro', markersize=3)

        #Draw center of mass (COM) of the container
        com = visualisation_object.com
        plt.scatter(com[0], com[1], marker='x', color='red', s=100)

        #Plot formatting
        ax.set_xlim(-5, visualisation_object.container_width + 5)
        ax.set_ylim(-5, visualisation_object.container_height + 5)
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(f"Best Member (Gen {generation if generation is not None else '?'})")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.show()