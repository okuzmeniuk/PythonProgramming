class Worker:
    id_count = 0

    def __init__(self, name, surname, department, salary):
        self.__id = Worker.id_count
        Worker.id_count += 1
        self.name = name
        self.surname = surname
        self.department = department
        self.salary = round(float(salary), 2)

    def get_id(self):
        return self.__id

    def __repr__(self):
        output = ""
        output += f"{self.get_id()},"
        output += f"{self.name},"
        output += f"{self.surname},"
        output += f"{self.department},"
        output += f"{self.salary}"
        return output

    def __str__(self):
        output = ""
        output += f"ID: {self.get_id()}\n"
        output += f"Name: {self.name}\n"
        output += f"Surname: {self.surname}\n"
        output += f"Department: {self.department}\n"
        output += f"Salary: {self.salary}"
        return output

    def __getitem__(self, item):
        if item == 'id' or item == '_Worker__id':
            raise ValueError("id is a private field")

        if item not in vars(self):
            raise ValueError(f"{item} is not a field of class instance")

        return vars(self)[item]

    def __setitem__(self, key, value):
        if key == 'id' or key == '_Worker__id':
            raise ValueError("id is a private field")

        if key not in vars(self):
            raise ValueError(f"{key} is not a field of class instance")

        if key == "salary":
            value = round(float(value), 2)

        vars(self)[key] = value

    @classmethod
    def from_console(cls):
        name = input("Enter worker name: ")
        surname = input("Enter worker surname: ")
        department = input("Enter worker department: ")
        salary = input("Enter salary: ")
        return cls(name, surname, department, salary)
