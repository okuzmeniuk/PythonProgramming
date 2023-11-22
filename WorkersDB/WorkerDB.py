import csv
from Worker import Worker


def dec_sort(method):
    def wrapper(self, key, descending):
        print(f"Sorted by {key}:")
        return method(self, key, descending)

    return wrapper


def dec_search(method):
    def wrapper(self, key, keyword):
        print(f"Searched in {key} with {keyword}:")

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
    def sort(self, key, descending=False):
        self.database.sort(key=lambda worker: worker[key], reverse=descending)

    @dec_search
    def search(self, key, keyword):
        results = WorkerDB()

        for worker in self.database:
            if keyword in str(worker[key]):
                results.add(worker)

        return results
