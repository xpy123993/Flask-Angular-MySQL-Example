"""
IO Packages for this webapp.

Person: Basic data structure.
Storage: A basic storage adapter to do Load/Save/Update/Index operations.
"""
import json
import mysql.connector


def SerializeHub(persons):
    return json.dumps({'data': [x.serialize() for x in persons]})


def DeserializeHub(data):
    persons = json.loads(data)['data']
    return [Person(x['pid'], x['name'], x['age'], x['phone']) for x in persons]


def GenerateFakePersons(num):
    return [Person(
        pid=i,
        name='Person - %d' % i,
        phone='10086%d' % i,
        age=11 + i) for i in range(num)]


class Person:
    def __init__(self, pid, name, age, phone):
        self.pid = pid
        self.name = name
        self.age = age
        self.phone = phone

    def serialize(self):
        return {
            'pid': self.pid,
            'name': self.name,
            'age': self.age,
            'phone': self.phone
        }

    def __str__(self):
        return f'[Person ID: {self.pid}, Name: {self.name}, Age: {self.age}, Phone: {self.phone}]'


class Storage:
    def Load(self):
        raise Exception('not implemented')

    def Save(self, persons):
        raise Exception('not implemented')


class InMemoryStorage(Storage):
    def __init__(self, data=GenerateFakePersons(5)):
        self.data = data

    def _locate(self, pid):
        for i, p in enumerate(self.data):
            if pid == p.pid:
                return i
        return -1

    def Load(self):
        return self.data

    def Save(self, persons):
        self.data = persons


class MySQLStorage(Storage):
    def __init__(self, host, database, username, password):
        self.db = mysql.connector.connect(
            host=host,
            database=database,
            user=username,
            password=password,
        )
        self._initDB()

    def _initDB(self):
        cursor = self.db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS persons(pid int primary key, name varchar(256), age int, phone varchar(256))')

    def Load(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * from persons')
        return [Person(pid=x[0], name=x[1], age=x[2], phone=x[3]) for x in cursor.fetchall()]

    def _clear(self):
        cursor = self.db.cursor()
        cursor.execute('DELETE FROM persons')
        self.db.commit()

    def Save(self, persons):
        self._clear()
        cursor = self.db.cursor()
        sql = 'INSERT into persons (pid, name, age, phone) VALUES (%s, %s, %s, %s)'
        data = [(person.pid, person.name, person.age, person.phone)
                for person in persons]
        cursor.executemany(sql, data)
        self.db.commit()
        return cursor.rowcount
