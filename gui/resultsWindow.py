import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Algorithms.Algorithm_Greedy import Algorithm_Greedy
from Algorithms.Algorithm_Random import Algorithm_Random
from Algorithms.Container_Context import Container_Context
from Algorithms.Visualisation.Visualisation_Object import Visualisation_Object
from Algorithms.Visualisation.Custom_Visualisation import Custom_Visualisation
from ConsoleRedirect import ConsoleRedirect
import sys
from gui.HistoryRecord import HistoryRecord
import io, base64
import Algorithms.Operators.penalty_functions as penalty_functions
from Algorithms.Vector2 import Vector2
import Algorithms.Visualisation.Results_Graphs as Results_Graphs
import threading

#Responsible for rendering and interaction of the GUI. The GUI allows the user to switch between algorithms and view the results in realtime.
class AlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithms and Results")
        
        self.algorithms = ["Greedy", "Random", "Cartesian GA", "Order-Based GA"]
        self.current_algorithm_index = 0

        self.test_cases = ["Test Case 1", "Test Case 2", "Test Case 3"]
        self.current_test_case_index = 0

        left_frame = ttk.Frame(root, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_frame, text="Algorithms", font=("Arial", 12, "bold")).pack(pady=5)

        self.algorithms_listbox = tk.Listbox(left_frame, height=10, exportselection=False)
        self.test_cases_listbox = tk.Listbox(left_frame, height=10, exportselection=False)
        
        for algo in self.algorithms:
            self.algorithms_listbox.insert(tk.END, algo)

        for test_case in self.test_cases:
            self.test_cases_listbox.insert(tk.END, test_case)
            
        #Selectbox so the users can see all the algorithms and can select specific ones.
        self.algorithms_listbox.selection_set(self.current_algorithm_index)
        self.algorithms_listbox.bind("<<ListboxSelect>>", self.on_algorithm_listbox_select)
        self.algorithms_listbox.pack(pady=5, fill=tk.BOTH)

        #Selectbox so the users can see all the different circle test cases and can select specific ones.
        self.test_cases_listbox.selection_set(self.current_test_case_index)
        self.test_cases_listbox.bind("<<ListboxSelect>>", self.on_case_listbox_select)
        self.test_cases_listbox.pack(pady=5, fill=tk.BOTH)

        arrows_frame = ttk.Frame(left_frame)
        arrows_frame.pack(pady=10)

        self.run_button = ttk.Button(arrows_frame, text="Run", command=self.run_algorithm)
        self.run_button.pack(side=tk.TOP, padx=5)

        #This is where the matplotlib results will be embedded.
        right_frame = ttk.Frame(root, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="Results", font=("Arial", 12, "bold")).pack(pady=5)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab0 = ttk.Frame(self.notebook)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        #Setup the console to tab0
        self.console_text = tk.Text(self.tab0, wrap="word", height=20,)
        self.console_text.pack(fill="both", expand=True)
        self.console_text.config(state=tk.DISABLED)

        #Redirect stdout to use the tab0 console
        sys.stdout = ConsoleRedirect(self.console_text)
        sys.stderr = ConsoleRedirect(self.console_text)

        self.notebook.add(self.tab0, text="Console")
        self.notebook.add(self.tab1, text="Visual Container")
        self.notebook.add(self.tab2, text="Fitness Over Gens")

        self.history:dict[str, HistoryRecord] = {}

        self.initialise_history()

        self.poll_console()

    def poll_console(self):
        self.console_text.update_idletasks()
        self.root.after(10, self.poll_console)  #Poll console every 10ms

    def embed_chart(self, b64, tab):
        for widget in tab.winfo_children():
            widget.destroy()

        if not b64:
            return
        
        img = tk.PhotoImage(data=b64)

        #Create storage dict on first use
        if not hasattr(self, "_image_refs"):
            self._image_refs = {}  #dictionary, not a list to avoid memory leaks

        #Replace any existing reference for this tab
        self._image_refs[tab] = img

        label = ttk.Label(tab, image=img)
        label.pack(fill="both", expand=True)

    def update_tab_content(self, selected_algorithm, selected_case):
        key = f"{selected_algorithm}_{selected_case}"

        if key in self.history:
            loaded_history = self.history[key]
            
            #Console (tab0)
            self.console_text.delete("1.0", "end")
            self.notebook.select(self.tab0)
            print(loaded_history.console_history)

            #Container Visualisation (tab1)
            self.embed_chart(loaded_history.visualisation_history, self.tab1)

            #Fitnesses over generations (tab2)
            self.embed_chart(loaded_history.fitness_history, self.tab2)

    #Initialises the history by creating an entry for each algorithm_case composite key
    def initialise_history(self):
        for algo in self.algorithms:
            for case in self.test_cases:
                self.history[f"{algo}_{case}"] = HistoryRecord(f"{algo} for {case} has not been run yet", None, None)

    def on_algorithm_listbox_select(self, event):
        selection = self.algorithms_listbox.curselection()
        
        if selection:
            self.current_algorithm_index = selection[0]
            self.update_plot()

    def on_case_listbox_select(self, event):
        selection = self.test_cases_listbox.curselection()
        
        if selection:
            self.current_test_case_index = selection[0]
            self.update_plot()

    def update_plot(self):
        algo_name = self.algorithms[self.current_algorithm_index]
        case_name = self.test_cases[self.current_test_case_index]

        self.update_tab_content(algo_name, case_name)

    def run_algorithm(self):
        thread = threading.Thread(target=self._run_algorithm_worker)
        thread.daemon = True
        thread.start()

    def _run_algorithm_worker(self):
        algo_name = self.algorithms[self.current_algorithm_index]
        case_name = self.test_cases[self.current_test_case_index]

        best_fitnesses = []

        if algo_name == "Greedy":
            print("===== RUNNING GREEDY ALGORITHM =====")

            container = Container_Context(30, 15)
            algorithm = Algorithm_Greedy(container, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300])
            algorithm.run()
            best_fitness = algorithm.calculate_fitness()

            print(f"Overall Fitness: {best_fitness}")

            vector2pos = []
            pos = []

            for i in algorithm.placed_circles:
                vector2pos.append(Vector2(i[0], i[1]))
                pos.append((i[0], i[1]))

            com = penalty_functions.calculate_com_penalty(vector2pos, algorithm.masses, Vector2(container.container_width / 2, container.container_height / 2))[0]
            cb = Visualisation_Object(pos, algorithm.radii, algorithm.masses, [com.x, com.y], algorithm.container_context.container_width, algorithm.container_context.container_height)
            c = Custom_Visualisation()
            fig, ax = c.visualise(cb, self_display=False)

            best_fitnesses = [best_fitness]

        elif algo_name == "Random":
            print("===== RUNNING RANDOM ALGORITHM =====")

            container = Container_Context(30, 15)
            algorithm = Algorithm_Random([2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300], container.container_width, container.container_height, 10000)
            algorithm.run()
            best_member = algorithm.best
            best_fitness = algorithm.best_fitness

            print(f"Overall Fitness: {best_fitness}")

            vector2pos = []
            pos = []

            for gene in best_member.genome: #type: ignore
                pos.append([gene.position.x, gene.position.y])
                vector2pos.append(gene.position)

            com = penalty_functions.calculate_com_penalty(vector2pos, algorithm.masses, Vector2(container.container_width / 2, container.container_height / 2))[0]
            cb = Visualisation_Object(pos, algorithm.radii, algorithm.masses, [com.x, com.y], algorithm.container_width, algorithm.container_height)
            c = Custom_Visualisation()
            fig, ax = c.visualise(cb, self_display=False)

            best_fitnesses = [best_fitness]

        #Set History
        key = f"{algo_name}_{case_name}"

        self.history[key].console_history = self.console_text.get("1.0", "end")
        self.history[key].visualisation_history = self.fig_to_base64(fig) #type: ignore
        self.history[key].fitness_history = self.fig_to_base64(Results_Graphs.draw_fitness_over_gens(best_fitnesses, display=False))

        self.update_plot()

    def fig_to_base64(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0.3) #type: ignore
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("ascii")

        return b64

def show_window():
    root = tk.Tk()
    app = AlgorithmGUI(root)
    root.mainloop()