import sys
import tkinter as tk
from tkinter import ttk

class ConsoleRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert("end", message)
        self.text_widget.see("end")  #auto-scroll
        self.text_widget.config(state=tk.DISABLED)

    def flush(self):
        pass