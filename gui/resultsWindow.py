import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Algorithms.Algorithm_Greedy import Algorithm_Greedy
from Algorithms.Container_Context import Container_Context
from Algorithms.Visualisation.Visualisation_Object import Visualisation_Object
from Algorithms.Visualisation.Custom_Visualisation import Custom_Visualisation
from ConsoleRedirect import ConsoleRedirect
import sys
from gui.HistoryRecord import HistoryRecord
import io, base64

#Responsible for rendering and interaction of the GUI. The GUI allows the user to switch between algorithms and view the results in realtime.
class AlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithms and Results")
        
        self.algorithms = ["Greedy", "Random", "Cartesian GA", "Order-Based GA"]
        self.ran_algorithms = []
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

        #These are the buttons which allow the user to easily toggle between algorithms.
        self.prev_button = ttk.Button(arrows_frame, text="← Prev Algorithm", command=self.prev_algorithm)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(arrows_frame, text="Next Algorithm →", command=self.next_algorithm)
        self.next_button.pack(side=tk.LEFT, padx=5)

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
        self.console_text = tk.Text(self.tab0, wrap="word", height=20)
        self.console_text.pack(fill="both", expand=True)

        #Redirect stdout to use the tab0 console
        sys.stdout = ConsoleRedirect(self.console_text)
        sys.stderr = ConsoleRedirect(self.console_text)

        self.notebook.add(self.tab0, text="Console")
        self.notebook.add(self.tab1, text="Visual Container")
        self.notebook.add(self.tab2, text="Time Taken")
        self.notebook.add(self.tab3, text="Some Other Metric")

        self.history:dict[str, HistoryRecord] = {}

        self.initialise_history()

    def embed_chart(self, b64, tab):
        for widget in tab.winfo_children():
            widget.destroy()

        if not b64:
            return
        
        img = tk.PhotoImage(data=b64)

        #Create storage dict on first use
        if not hasattr(self, "_image_refs"):
            self._image_refs = {}  # dictionary, not a list

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

    #Initialises the history by creating an entry for each algorithm_case composite key
    def initialise_history(self):
        for algo in self.algorithms:
            for case in self.test_cases:
                self.history[f"{algo}_{case}"] = HistoryRecord(f"{algo}_{case} has not been run yet", None)

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

    def prev_algorithm(self):
        if self.current_algorithm_index > 0:
            self.current_algorithm_index -= 1
        else:
            self.current_algorithm_index = len(self.algorithms) - 1
            
        self.algorithms_listbox.selection_clear(0, tk.END)
        self.algorithms_listbox.selection_set(self.current_algorithm_index)
        self.algorithms_listbox.see(self.current_algorithm_index)
        self.update_plot()

    def next_algorithm(self):
        if self.current_algorithm_index < len(self.algorithms) - 1:
            self.current_algorithm_index += 1
        else:
            self.current_algorithm_index = 0
            
        self.algorithms_listbox.selection_clear(0, tk.END)
        self.algorithms_listbox.selection_set(self.current_algorithm_index)
        self.algorithms_listbox.see(self.current_algorithm_index)
        self.update_plot()

    def update_plot(self):
        algo_name = self.algorithms[self.current_algorithm_index]
        case_name = self.test_cases[self.current_test_case_index]

        self.update_tab_content(algo_name, case_name)

    def run_algorithm(self):
        algo_name = self.algorithms[self.current_algorithm_index]
        case_name = self.test_cases[self.current_test_case_index]

        if algo_name == "Greedy":
            print("===== RUNNING GREEDY ALGORITHM =====")

            c = Container_Context(30, 15)
            a = Algorithm_Greedy(c, [2.0, 2.0, 1.5, 1.5, 1.2, 2.0, 1.5, 2.0, 1.5, 2.0, 1.2, 1.2, 1.2, 1.2], [2500, 2500, 800, 800, 300, 2500, 800, 2500, 800, 2500, 300, 300, 300, 300])
            a.run()

            print(f"Overall Fitness: {a.calculate_fitness()}")

            pos = []

            for i in a.placed_circles:
                pos.append((i[0], i[1]))

            com = [0, 0]
            #com = penalty_functions.calculate_com_penalty(a.placed_circles, a.masses, Vector2(a.container_width / 2, a.container_height / 2))[0]
            cb = Visualisation_Object(pos, a.radii, a.masses, com, a.container_context.container_width, a.container_context.container_height)
            c = Custom_Visualisation()
            fig, ax = c.visualise(cb, self_display=False)

            self.embed_chart(self.fig_to_base64(fig), self.tab1)
            
            if "Greedy" not in self.ran_algorithms:
                self.ran_algorithms.append("Greedy")

        #Set History
        key = f"{algo_name}_{case_name}"

        self.history[key].console_history = self.console_text.get("1.0", "end")
        self.history[key].visualisation_history = self.fig_to_base64(fig) #type: ignore

    def fig_to_base64(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0) #type: ignore
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("ascii")

        return b64

def show_window():
    root = tk.Tk()
    app = AlgorithmGUI(root)
    root.mainloop()