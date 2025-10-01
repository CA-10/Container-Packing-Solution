import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#Responsible for rendering and interaction of the GUI. The GUI allows the user to switch between algorithms and view the results in realtime.
class AlgorithmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithms and Results")
        
        self.algorithms = ["Evolutionary Algorithm", "Heuristic Approach", "Algorithm C", "Algorithm D"]
        self.current_index = 0

        left_frame = ttk.Frame(root, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_frame, text="Algorithms", font=("Arial", 12, "bold")).pack(pady=5)

        self.listbox = tk.Listbox(left_frame, height=10, exportselection=False)
        
        for algo in self.algorithms:
            self.listbox.insert(tk.END, algo)
            
        #This is a selectbox so the users can see all the algorithms and can select specific ones.
        self.listbox.selection_set(self.current_index)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.listbox.pack(pady=5, fill=tk.BOTH)

        arrows_frame = ttk.Frame(left_frame)
        arrows_frame.pack(pady=10)

        #These are the buttons which allow the user to easily toggle between algorithms.
        self.prev_button = ttk.Button(arrows_frame, text="← Prev", command=self.prev_algorithm)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(arrows_frame, text="Next →", command=self.next_algorithm)
        self.next_button.pack(side=tk.LEFT, padx=5)

        #This is where the matplotlib results will be embedded.
        right_frame = ttk.Frame(root, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="Results", font=("Arial", 12, "bold")).pack(pady=5)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Tabs
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)

        notebook.add(tab1, text="Visual Container")
        notebook.add(tab2, text="Time Taken")
        notebook.add(tab3, text="Some Other Metric")

        #This is a placeholder chart. Embed the real charts later. This needs to be dependant on the selected tab.
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot([0, 1, 2, 3], [0, 1, 0, 1], label="Placeholder")
        ax.legend()
        
        #Embed the chart into the canvas.
        canvas = FigureCanvasTkAgg(figure, master=tab1) 
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_listbox_select(self, event):
        selection = self.listbox.curselection()
        
        if selection:
            self.current_index = selection[0]
            self.update_plot()

    def prev_algorithm(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.algorithms) - 1
            
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.listbox.see(self.current_index)
        self.update_plot()

    def next_algorithm(self):
        if self.current_index < len(self.algorithms) - 1:
            self.current_index += 1
        else:
            self.current_index = 0
            
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.listbox.see(self.current_index)
        self.update_plot()

    def update_plot(self):
        algo_name = self.algorithms[self.current_index]
        self.ax.clear()
        
        #PLACEHOLDER - REPLACE.
        if algo_name == "Algorithm A":
            self.ax.plot([1,2,3,4], [1,4,9,16], 'r-', label="Squares")
        elif algo_name == "Algorithm B":
            self.ax.plot([1,2,3,4], [1,2,3,4], 'g--', label="Linear")
        elif algo_name == "Algorithm C":
            self.ax.plot([1,2,3,4], [1,0,1,0], 'b:', label="Oscillate")
        else:
            self.ax.bar([1,2,3], [3,2,5], label="Bars")

        self.ax.set_title(algo_name)
        self.ax.legend()
        self.canvas.draw()

def show_window():
    root = tk.Tk()
    app = AlgorithmGUI(root)
    root.mainloop()