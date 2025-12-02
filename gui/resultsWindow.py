import tkinter as tk
from tkinter import font
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Algorithms.Algorithm_Greedy import Algorithm_Greedy
from Algorithms.Algorithm_Random import Algorithm_Random
from Algorithms.Algorithm_GA import Algorithm_GA
from Algorithms.Algorithm_Hybrid import Algorithm_Hybrid
from Algorithms.Container_Context import Container_Context
from Algorithms.Visualisation.Visualisation_Object import Visualisation_Object
from Algorithms.Visualisation.Custom_Visualisation import Custom_Visualisation
import sys
from gui.HistoryRecord import HistoryRecord
import io, base64
import Algorithms.Operators.penalty_functions as penalty_functions
from Algorithms.Vector2 import Vector2
import Algorithms.Visualisation.Results_Graphs as Results_Graphs
import threading
import test_cases as tests

#Responsible for rendering and interaction of the GUI. The GUI allows the user to switch between algorithms and view the results in realtime.
class AlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithms and Results")
        
        self.algorithms = ["Greedy", "Random", "Cartesian GA", "Order-Based GA"]
        self.current_algorithm_index = 0

        self.test_cases = [k for k in tests.test_cases.keys()]
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

        self.run_all_button = ttk.Button(arrows_frame, text="Run All For Test Case", command=self.run_all)
        self.run_all_button.pack(side=tk.TOP, padx=5, pady=10)

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
        my_font = font.Font(family="Courier New", size=16)
        self.console_text = tk.Text(self.tab0, wrap="word", height=20, font=my_font)
        self.console_text.pack(fill="both", expand=True)
        self.console_text.config(state=tk.DISABLED)

        self.notebook.add(self.tab0, text="Stats")
        self.notebook.add(self.tab1, text="Visual Container")
        self.notebook.add(self.tab2, text="Fitness Over Gens")

        self.history:dict[str, HistoryRecord] = {}

        self.initialise_history()

    def insert_text(self, text):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete("1.0", "end")
        self.console_text.insert("1.0", text)
        self.console_text.config(state=tk.DISABLED)

    def embed_chart(self, b64, tab):
        # Clear previous widgets
        for widget in tab.winfo_children():
            widget.destroy()

        if not b64:
            return

        # Create storage dict on first use
        if not hasattr(self, "_image_refs"):
            self._image_refs = {}

        # Convert base64 to PhotoImage
        img = tk.PhotoImage(data=b64)

        # Keep a reference to avoid garbage collection
        self._image_refs[tab] = img

        # Create a canvas to hold the image
        canvas = tk.Canvas(tab)
        canvas.pack(fill="both", expand=True, side="left")

        # Add scrollbars
        v_scroll = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        v_scroll.pack(fill="y", side="right")
        h_scroll = ttk.Scrollbar(tab, orient="horizontal", command=canvas.xview)
        h_scroll.pack(fill="x", side="bottom")

        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Create an inner frame to hold the label
        frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Add the image to the frame
        label = ttk.Label(frame, image=img)
        label.pack()

        # Update scroll region whenever size changes
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

    def update_tab_content(self, selected_algorithm, selected_case):
        key = f"{selected_algorithm}_{selected_case}"

        if key in self.history:
            loaded_history = self.history[key]
            
            #Console (tab0)
            self.insert_text(loaded_history.console_history)

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

    def run_all(self):
        thread = threading.Thread(target=self._run_all_worker)
        thread.daemon = True
        thread.start()
        
    def run_and_eval_algo(self, algo_name, case_name):
        best_fitnesses = []
        test_case = tests.test_cases[case_name]

        if not test_case:
            return

        #Show the stats tab when running
        self.notebook.select(self.tab0)

        if algo_name == "Greedy":
            print("===== RUNNING GREEDY ALGORITHM =====")
            self.insert_text("RUNNING GREEDY ALGORITHM. PLEASE CHECK CONSOLE FOR UPDATES")

            container = Container_Context(test_case.container_width, test_case.container_height)
            algorithm = Algorithm_Greedy(container, test_case.radii, test_case.masses)
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
            self.insert_text("RUNNING RANDOM ALGORITHM. PLEASE CHECK CONSOLE FOR UPDATES")

            container = Container_Context(test_case.container_width, test_case.container_height)
            algorithm = Algorithm_Random(test_case.radii, test_case.masses, container.container_width, container.container_height, 1000)
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

        elif algo_name == "Cartesian GA":
            print("===== RUNNING CARTESIAN GA ALGORITHM =====")
            self.insert_text("RUNNING CARTESIAN GA ALGORITHM. PLEASE CHECK CONSOLE FOR UPDATES")

            container = Container_Context(test_case.container_width, test_case.container_height)
            algorithm = Algorithm_GA(1000, 500, 0.03, container.container_width, container.container_height, test_case.radii, test_case.masses, "tournament", 8)
            algorithm.run()

            best_member = algorithm.population.population[algorithm.population.fitnesses.index(max(algorithm.population.fitnesses))].genome

            positions = []
            vector2positions = []

            for gene in best_member:
                positions.append([gene.position.x, gene.position.y])
                vector2positions.append(gene.position)

            com = penalty_functions.calculate_com_penalty(vector2positions, algorithm.masses, Vector2(container.container_width / 2, container.container_height / 2))[0]
            cb = Visualisation_Object(positions, algorithm.radii, algorithm.masses, [com.x, com.y], algorithm.container_width, algorithm.container_height)
            c = Custom_Visualisation()
            fig, ax = c.visualise(cb, self_display=False)
            best_fitnesses = list(algorithm.best_fitnesses)

        elif algo_name == "Order-Based GA":
            print("===== RUNNING ORDER-BASED GA ALGORITHM =====")
            self.insert_text("RUNNING ORDER-BASED GA GA ALGORITHM. PLEASE CHECK CONSOLE FOR UPDATES")

            container = Container_Context(test_case.container_width, test_case.container_height)
            algorithm = Algorithm_Hybrid(300, 100, 0.03, container.container_width, container.container_height, test_case.radii, test_case.masses, "tournament", 8)
            algorithm.run()

            best_member = algorithm.population.population[algorithm.population.fitnesses.index(max(algorithm.population.fitnesses))].genome

            positions = []
            vector2positions = []

            for gene in best_member:
                positions.append([gene.position.x, gene.position.y])
                vector2positions.append(gene.position)

            com = penalty_functions.calculate_com_penalty(vector2positions, algorithm.masses, Vector2(container.container_width / 2, container.container_height / 2))[0]
            cb = Visualisation_Object(positions, algorithm.radii, algorithm.masses, [com.x, com.y], algorithm.container_width, algorithm.container_height)
            c = Custom_Visualisation()
            fig, ax = c.visualise(cb, self_display=False)
            best_fitnesses = list(algorithm.best_fitnesses)

        stats = algorithm.print_stats() #type: ignore

        stats_text = (
            f"====={algo_name.upper()} ALGORITHM STATS=====\n"
            f"Runtime Seconds (s): {stats[0]}\n"
            f"Total Iterations/Generations: {stats[1]}\n"
            f"Fitness: {stats[2]}\n"
        )

        #Set History
        key = f"{algo_name}_{case_name}"

        self.history[key].console_history = stats_text
        self.history[key].visualisation_history = self.fig_to_base64(fig) #type: ignore
        self.history[key].fitness_history = self.fig_to_base64(Results_Graphs.draw_fitness_over_gens(best_fitnesses, display=False))

        self.update_plot()

    def _run_algorithm_worker(self):
        algo_name = self.algorithms[self.current_algorithm_index]
        case_name = self.test_cases[self.current_test_case_index]

        self.run_and_eval_algo(algo_name, case_name)

    def _run_all_worker(self):
        case_name = self.test_cases[self.current_test_case_index]

        for i in range(len(self.algorithms)):
            self.current_algorithm_index = i

            self.algorithms_listbox.selection_clear(0, tk.END)
            self.algorithms_listbox.selection_set(self.current_algorithm_index)
            self.algorithms_listbox.see(self.current_algorithm_index)

            self.run_and_eval_algo(self.algorithms[self.current_algorithm_index], case_name)

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