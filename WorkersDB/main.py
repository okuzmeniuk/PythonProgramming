from menu import Menu
from WorkerDB import WorkerDB
from Worker import Worker


def read_from_file(worker_db):
    print("Reading the data...")

    try:
        worker_db.read_csv()
    except Exception as exc:
        print(exc)
        return

    print("Done...")


def add_element_from_console(worker_db):
    try:
        element = Worker.from_console()
    except Exception as exc:
        print(exc)
        return

    worker_db.add(element)


def search(worker_db):
    key = input("Enter key to search by (id, name, surname, department, salary): ")
    keyword = input("Enter keyword to search: ")

    try:
        result = worker_db.search(key, keyword)
    except Exception as exc:
        print(exc)
        return

    if len(result) == 0:
        print("No results")
    else:
        print(result)


def sort(worker_db):
    if len(worker_db) == 0:
        print("The database is empty")
        return

    key = input("Enter key to sort by (id, name, surname, department, salary): ")
    try:
        worker_db.sort(key)
    except Exception:
        pass


def delete_element(worker_db):
    id_to_delete = int(input("Enter ID to delete: "))
    try:
        worker_db.delete(id_to_delete)
    except Exception as exc:
        print(exc)


def edit_element(worker_db):
    id_to_edit = int(input("Enter ID to edit: "))
    key_to_edit = input("Enter key to edit (id, name, surname, department, salary): ")
    new_value = input("Enter new value: ")
    try:
        worker_db.edit(id_to_edit, key_to_edit, new_value)
    except Exception as exc:
        print(exc)


def main():
    worker_db = WorkerDB('workers_to_read.csv')

    menu_options = {
        '1': "print the database",
        '2': "read from the file",
        '3': "add worker from console",
        '4': "use the search",
        '5': "use the sort",
        '6': "delete the element by ID",
        '7': "change element by ID"
    }

    menu_functions = {
        '1': lambda db: print(db),
        '2': read_from_file,
        '3': add_element_from_console,
        '4': search,
        '5': sort,
        '6': delete_element,
        '7': edit_element
    }

    Menu(menu_options, menu_functions).run(worker_db)


if __name__ == "__main__":
    main()
