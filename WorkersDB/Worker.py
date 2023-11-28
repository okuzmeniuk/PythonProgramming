def id_generator():
    _id = 0

    while True:
        yield _id
        _id += 1


class Worker:
    id_gen = id_generator()

    def __init__(self, name, surname, department, salary):
        self.name = name
        self.surname = surname
        self.department = department
        self.salary = salary
        self.__id = next(Worker.id_gen)

    def get_id(self):
        return self.__id

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        self._salary = round(float(value), 2)

    def __repr__(self):
        output = ""
        output += f"{self.get_id()},"
        output += f"{self.name},"
        output += f"{self.surname},"
        output += f"{self.department},"
        output += f"{self.salary:.2f}"
        return output

    def __str__(self):
        output = ""
        output += f"ID: {self.get_id()}\n"
        output += f"Name: {self.name}\n"
        output += f"Surname: {self.surname}\n"
        output += f"Department: {self.department}\n"
        output += f"Salary: {self.salary:.2f}"
        return output

    def __getitem__(self, item):
        if item == 'id':
            return self.get_id()

        if item == "salary":
            return self.salary

        if item not in vars(self):
            raise ValueError(f"{item} is not a field of class instance")

        return vars(self)[item]

    def __setitem__(self, key, value):
        if key == 'id' or key == '_Worker__id':
            raise ValueError("id is a private field")

        if key == "salary":
            self.salary = round(float(value), 2)
            return

        if key not in vars(self):
            raise ValueError(f"{key} is not a field of class instance")

        vars(self)[key] = value

    @classmethod
    def from_console(cls):
        name = input("Enter worker name: ")
        surname = input("Enter worker surname: ")
        department = input("Enter worker department: ")
        salary = input("Enter salary: ")
        return cls(name, surname, department, salary)
