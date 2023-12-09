from Worker import Worker
from WorkerDB import WorkerDB
import tkinter as tk
from tkinter import ttk


class WorkerApp:
    def __init__(self, root):
        self.worker_db = WorkerDB('workers_to_read.csv')
        self.root = root
        self.root.title("WorkersDB")
        self.root.resizable(False, False)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side=tk.LEFT, anchor='nw', padx=10, pady=10)
        self.create_buttons()

        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(side=tk.LEFT, anchor='ne', padx=10, pady=10)
        self.text_scrollbar = tk.Scrollbar(self.text_frame, orient='vertical')
        self.text_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.output_text = tk.Text(self.text_frame, font=("Cascadia Mono", 12),
                                   yscrollcommand=self.text_scrollbar.set, cursor="arrow")
        self.output_text.config(state=tk.DISABLED)
        self.text_scrollbar.config(command=self.output_text.yview)
        self.output_text.pack(side=tk.LEFT, padx=5, pady=5)

    def create_buttons(self):
        buttons_names_and_commands = {
            "Print the database": self.print_database,
            "Read from the file": self.read_from_file,
            "Add new worker": self.add_worker_window,
            "Edit worker info by ID": self.edit_worker_window,
            "Delete the element by ID": self.delete_worker_window,
            "Search": self.search_window,
            "Sort": self.sort_window,
            "Plot a departments diagram": self.worker_db.department_pie_plot
        }

        for name, command in buttons_names_and_commands.items():
            button = ttk.Button(self.buttons_frame, text=name, command=command)
            button.pack(side=tk.TOP, anchor='nw', padx=5, pady=5)

    def print_to_output(self, to_print):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, str(to_print) + '\n')
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see("end")

    def print_database(self):
        self.print_to_output(self.worker_db)
        self.print_to_output('=' * 50)

    def read_from_file(self):
        self.print_to_output("Reading the data...")

        try:
            self.worker_db.read_csv()
        except Exception as exc:
            print(exc)
            return

        self.print_to_output("Done...")
        self.print_to_output('=' * 50)

    def add_worker(self, data):
        try:
            worker_to_add = Worker(*data)
            self.worker_db.add(worker_to_add)
            self.print_to_output("Successfully added new worker.")
        except Exception as exc:
            self.print_to_output(exc)

        self.print_to_output('=' * 50)

    def add_worker_window(self):
        input_window = InputWindow("Input worker info", self.add_worker)
        input_window.add_input_field("Name")
        input_window.add_input_field("Surname")
        input_window.add_input_field("Department")
        input_window.add_input_field("Salary")

    def edit_worker(self, data):
        try:
            self.worker_db.edit(*data)
            self.print_to_output("Successfully changed.")
        except Exception as exc:
            self.print_to_output(exc)

        self.print_to_output('=' * 50)

    def edit_worker_window(self):
        input_window = InputWindow("Input edit info", self.edit_worker)
        input_window.add_input_field("ID to edit")
        input_window.add_input_field("Key to edit (id, name, surname, department, salary)")
        input_window.add_input_field("New value")

    def delete_worker(self, data):
        id_to_delete = int(data[0])
        try:
            self.worker_db.delete(id_to_delete)
            self.print_to_output("Successfully deleted.")
        except Exception as exc:
            self.print_to_output(exc)

        self.print_to_output('=' * 50)

    def delete_worker_window(self):
        input_window = InputWindow("Input ID", self.delete_worker)
        input_window.add_input_field("ID of worker to delete")

    def search(self, data):
        key = data[0]
        keyword = data[1]

        try:
            result = self.worker_db.search(key, keyword)
        except Exception as exc:
            self.print_to_output(exc)
            self.print_to_output('=' * 50)
            return

        if len(result) == 0:
            self.print_to_output("No results")
        else:
            self.print_to_output(result)

        self.print_to_output('=' * 50)

    def search_window(self):
        input_window = InputWindow("Search info", self.search)
        input_window.add_input_field("Field to search in (id, name, surname, department, salary)")
        input_window.add_input_field("Keyword to search")

    def sort(self, data):
        key = data[0]
        try:
            self.worker_db.sort(key)
            self.print_to_output("Sorted successfully.")
        except ValueError as exc:
            self.print_to_output(exc)

        self.print_to_output('=' * 50)

    def sort_window(self):
        input_window = InputWindow("Sort info", self.sort)
        input_window.add_input_field("Key to sort by (id, name, surname, department, salary)")


class InputWindow(tk.Toplevel):
    def __init__(self, title, callback):
        super().__init__()
        self.resizable(False, False)
        self.title(title)
        self.callback = callback

        self.inputs_frame = tk.Frame(self)
        self.inputs_frame.pack(side=tk.TOP, padx=5, pady=5)
        self.input_entries = []

        self.done_button = ttk.Button(self, text="Done", command=self.done_pressed)
        self.done_button.pack(side=tk.TOP, padx=5, pady=5)

    def add_input_field(self, name):
        info_label = ttk.Label(self.inputs_frame, text=name)
        info_label.pack(side=tk.TOP, padx=5, pady=5)
        input_entry = ttk.Entry(self.inputs_frame, width=50)
        input_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.input_entries.append(input_entry)

    def done_pressed(self):
        input_data = [entry.get() for entry in self.input_entries]
        self.callback(input_data)
        self.destroy()
