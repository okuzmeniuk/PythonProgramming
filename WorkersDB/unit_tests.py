import unittest
from Worker import Worker, id_generator
from WorkerDB import WorkerDB


class TestWorkerMethods(unittest.TestCase):
    def setUp(self):
        self.real_id_generator_object = Worker.id_gen
        Worker.id_gen = id_generator()
        self.worker_object = Worker("Lorem", "Ipsum", "Janitor", 20000)

    def tearDown(self):
        Worker.id_gen = self.real_id_generator_object

    def test_get_id(self):
        self.assertEqual(self.worker_object.get_id(), 0)

    def test_repr_and_str(self):
        expected_repr = "0,Lorem,Ipsum,Janitor,20000.00"
        expected_str = ("ID: 0\n"
                        "Name: Lorem\n"
                        "Surname: Ipsum\n"
                        "Department: Janitor\n"
                        "Salary: 20000.00")

        self.assertEqual(repr(self.worker_object), expected_repr)
        self.assertEqual(str(self.worker_object), expected_str)

    def test_get_item_operator(self):
        self.assertEqual(self.worker_object['id'], 0)
        self.assertRaises(ValueError, self.worker_object.__getitem__, 'non-existent field')
        self.assertEqual(self.worker_object['name'], 'Lorem')
        self.assertEqual(self.worker_object['surname'], 'Ipsum')
        self.assertEqual(self.worker_object['department'], 'Janitor')
        self.assertEqual(self.worker_object['salary'], 20000.0)

    def test_set_item_operator(self):
        self.assertRaises(ValueError, self.worker_object.__setitem__, 'id', 'asd')
        self.assertRaises(ValueError, self.worker_object.__setitem__, '_Worker__id', 'dsa')
        self.assertRaises(ValueError, self.worker_object.__setitem__, 'non-existent field', 'some value')
        self.worker_object['name'] = '1'
        self.worker_object['surname'] = '2'
        self.worker_object['department'] = '3'
        self.assertRaises(ValueError, self.worker_object.__setitem__, 'salary', 'assadasd')
        self.worker_object['salary'] = 10000
        self.assertEqual(self.worker_object['name'], '1')
        self.assertEqual(self.worker_object['surname'], '2')
        self.assertEqual(self.worker_object['department'], '3')
        self.assertEqual(self.worker_object['salary'], 10000.0)


class TestWorkerDBMethods(unittest.TestCase):
    def setUp(self):
        self.real_id_generator_object = Worker.id_gen
        Worker.id_gen = id_generator()
        self.worker_db = WorkerDB()
        self.AMOUNT_OF_WORKERS = 10
        for i in range(self.AMOUNT_OF_WORKERS):
            self.worker_db.add(Worker(f"Lorem{i}", f"Ipsum{i}", f"Janitor{i}", 1000 * i))

    def tearDown(self):
        Worker.id_gen = self.real_id_generator_object

    def test_get_item_operator(self):
        for i in range(self.AMOUNT_OF_WORKERS):
            current_worker = self.worker_db[i]
            self.assertEqual(current_worker.get_id(), i)
            self.assertEqual(current_worker.name, f"Lorem{i}")
            self.assertEqual(current_worker.surname, f"Ipsum{i}")
            self.assertEqual(current_worker.department, f"Janitor{i}")
            self.assertEqual(current_worker.salary, 1000 * i)

    def test_str(self):
        worker_db_str = str(self.worker_db)
        expected_str = ''

        for i in range(self.AMOUNT_OF_WORKERS):
            expected_str += f"ID: {i}\n"
            expected_str += f"Name: Lorem{i}\n"
            expected_str += f"Surname: Ipsum{i}\n"
            expected_str += f"Department: Janitor{i}\n"
            expected_str += f"Salary: {1000 * i:.2f}\n\n"

        expected_str = expected_str[:-2]
        self.assertEqual(worker_db_str, expected_str)

    def test_empty_db_str(self):
        empty_db = WorkerDB()
        self.assertEqual(str(empty_db), "no records")

    def test_delete(self):
        self.assertRaises(IndexError, self.worker_db.delete, self.AMOUNT_OF_WORKERS * 10)
        self.worker_db.delete(0)
        self.AMOUNT_OF_WORKERS -= 1
        self.assertEqual(len(self.worker_db), self.AMOUNT_OF_WORKERS)
        self.assertEqual(self.worker_db[0], None)

    def test_edit(self):
        self.assertRaises(ValueError, self.worker_db.edit, 1, 'id', 0)
        self.worker_db.edit(1, 'name', '1')
        self.worker_db.edit(1, 'surname', '2')
        self.worker_db.edit(1, 'department', '3')
        self.assertRaises(ValueError, self.worker_db.edit, 1, 'salary', 'assadasd')
        self.worker_db.edit(1, 'salary', '10000')
        self.assertEqual(self.worker_db[1]['name'], '1')
        self.assertEqual(self.worker_db[1]['surname'], '2')
        self.assertEqual(self.worker_db[1]['department'], '3')
        self.assertEqual(self.worker_db[1]['salary'], 10000.0)

    def test_sort(self):
        self.assertRaises(ValueError, self.worker_db.sort, 'non-existent field')
        self.worker_db.sort('name')

        for i in range(self.AMOUNT_OF_WORKERS - 1):
            self.assertLessEqual(self.worker_db[i].name, self.worker_db[i + 1].name)

        self.worker_db.sort('salary')

        for i in range(self.AMOUNT_OF_WORKERS - 1):
            self.assertLessEqual(self.worker_db[i].salary, self.worker_db[i + 1].salary)

    def test_search(self):
        self.assertEqual(len(self.worker_db.search('name', 'a'*50)), 0)
        self.assertEqual(len(self.worker_db.search('surname', 'a' * 50)), 0)
        self.assertEqual(len(self.worker_db.search('department', 'a' * 50)), 0)
        self.assertEqual(len(self.worker_db.search('salary', 'a' * 50)), 0)
        self.assertEqual(len(self.worker_db.search('name', 'Lorem')), self.AMOUNT_OF_WORKERS)
        self.assertEqual(len(self.worker_db.search('salary', '200')), 1)


if __name__ == "__main__":
    unittest.main()
