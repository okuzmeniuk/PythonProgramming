import csv
from Worker import Worker
import matplotlib.pyplot as plt


def dec_sort(method):
    def wrapper(self, key):
        print(f"Trying to sort by {key}.")
        try:
            method(self, key)
            print("Success.")
        except ValueError as err:
            print("There was a problem: ", err)
            raise err

    return wrapper


def dec_search(method):
    def wrapper(self, key, keyword):
        print(f"Searched in {key} with {keyword}.")

        return method(self, key, keyword)

    return wrapper


class WorkerDB:
    def __init__(self, filepath=None):
        self.database = []
        self.filepath = filepath

    def __getitem__(self, item):
        for worker in self.database:
            if worker.get_id() == item:
                return worker

    def __str__(self):
        output = ""

        if len(self) == 0:
            return "no records"

        for worker in self.database:
            output += str(worker) + '\n\n'

        return output[:-2]

    def __len__(self):
        return len(self.database)

    def add(self, worker):
        self.database.append(worker)

    def read_csv(self):
        with open(self.filepath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                worker_to_add = Worker(**row)
                self.add(worker_to_add)

    def delete(self, id_to_delete):
        for i in range(len(self)):
            if self.database[i].get_id() == id_to_delete:
                self.database.pop(i)
                return

        raise IndexError(f"there is no worker with id={id_to_delete}")

    def edit(self, id_to_edit, key, new_value):
        self[id_to_edit][key] = new_value

    @dec_sort
    def sort(self, key):
        self.database.sort(key=lambda worker: worker[key])

    @dec_search
    def search(self, key, keyword):
        results = WorkerDB()

        for worker in self.database:
            if keyword in str(worker[key]):
                results.add(worker)

        return results

    def department_pie_plot(self):
        departments = {}

        for worker in self.database:
            current_department = worker.department

            if current_department not in departments:
                departments[current_department] = 1
            else:
                departments[current_department] += 1

        plt.pie(list(departments.values()), labels=list(departments.keys()))
        plt.savefig('departments.png')
