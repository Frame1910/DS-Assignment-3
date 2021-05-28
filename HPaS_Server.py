# Darren Meiring (10496696)
# Byron Gregoriadis (10497015)
import mysql.connector
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from mysql.connector import cursor

from mysql.connector.errors import ProgrammingError

print("Welcome to the Honours Pre-assessment System Server (HPaS Server)")


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class Database():  # * Goal of the Database class is to provide an interface for server-1 to interact with the MySQL database server (server-2)
    # * Goal of the constructor is to make sure a useable database is ready for use as well provide the rest of the class with a cursor object to execute queries
    def __init__(self, user, pwd, host="localhost", db="student_records"):
        try:
            self.cnx = mysql.connector.connect(
                user=user,
                password=pwd,
                host=host,
                database=db
            )
            self.cursor = self.cnx.cursor()
        except ProgrammingError:
            self.cursor = self.generateDatabase(user, pwd)

    # * Generates a new student_records database from scratch and returns a db cursor to execute queries
    def generateDatabase(self, user, pwd, host="localhost", db="student_records"):
        self.cnx = mysql.connector.connect(
            user=user,
            password=pwd,
            host=host
        )
        cursor = self.cnx.cursor()
        cursor.execute("CREATE DATABASE student_records")
        self.cnx.close()
        self.cnx = mysql.connector.connect(
            user=user,
            password=pwd,
            host=host,
            database=db
        )
        cursor = self.cnx.cursor()
        cursor.execute("CREATE TABLE students (id int PRIMARY KEY)")
        cursor.execute(
            "CREATE TABLE units (code varchar(255) PRIMARY KEY)")
        cursor.execute(
            "CREATE TABLE grades (id varchar(8), code varchar(255), mark int NOT NULL, PRIMARY KEY (id, code))")
        cursor.execute(
            "ALTER TABLE grades ADD FOREIGN KEY (id) REFERENCES students (id)")
        cursor.execute(
            "ALTER TABLE grades ADD FOREIGN KEY (code) REFERENCES units (code)")
        return cursor

    def getGrades(self, id):  # TODO: method to fetch a list of all grades for a particular student
        return cursor.execute("SELECT * FROM grades WHERE id=" + id)

    def addStudent(self, student_id):  # Method to add student record to database
        sql = 'INSERT INTO students (id) VALUES ("' + student_id + '")'
        self.cursor.execute(sql)
        self.cnx.commit()
        print(self.cursor.rowcount, "record inserted.")

    def addUnit(self, unit_code):  # Method to add unit record to database
        sql = 'INSERT INTO units (code) VALUES ("' + unit_code + '")'
        self.cursor.execute(sql)
        self.cnx.commit()
        print(self.cursor.rowcount, "record inserted.")

    def addGrade(self, id, code, grades):  # TODO: Write method to add grade record to database
        pass

    # * Checks how many unit grades a given student has
    def checkUnitCount(self, user_id):
        self.cursor.execute(
            "SELECT * FROM grades WHERE id ='" + str(user_id) + "'")
        return len(cursor)

    # ! Experimental modular method for queries
    def queryDB(self, table, attr=None, var=None, column="*"):
        if attr is None and var is None:
            return self.cursor.execute("SELECT " + column + " FROM " + table)
        else:
            return self.cursor.execute("SELECT " + column + " FROM " + table + " WHERE " + attr + "=" + str(var))


db = Database("root", "Letmein!1")
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def displayScores(person_info):
        units = person_info[1]
        for unit in units:
            print(unit[0], unit[1])
        return 0
    server.register_function(displayScores)

    def calculateGlobalAve(person_info):
        units = person_info[1]
        total = 0
        for unit in units:
            total += unit[1]
        return round(total/len(units), 2)
    server.register_function(calculateGlobalAve)

    def twelveHighest(person_info):
        scores_array = []
        units = person_info[1]
        for unit in units:
            scores_array.append(unit[1])
        scores_array.sort(reverse=True)
        return scores_array[0:12]
    server.register_function(twelveHighest)

    def calculateTopTwelveAves(person_info):
        arr = twelveHighest(person_info)
        total = sum(arr)
        return round(total/len(arr), 2)
    server.register_function(calculateTopTwelveAves)

    def determineHonours(person_info):
        global_ave = calculateGlobalAve(person_info)
        top_ave = calculateTopTwelveAves(person_info)
        if global_ave >= 70:
            return person_info[0] + ", " + str(global_ave) + ", QUALIFIED FOR HONOURS STUDY!"
        elif global_ave < 70 and top_ave >= 80:
            return person_info[0] + ", " + str(global_ave) + ", " + str(top_ave) + ", MAY HAVE GOOD CHANCE! Need further assessment!"
        elif global_ave < 70 and 70 <= top_ave <= 80:
            return person_info[0] + ", " + str(global_ave) + ", " + str(top_ave) + ", MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s special permission!"
        elif global_ave < 70 and top_ave < 70:
            return person_info[0] + ", " + str(global_ave) + ", " + str(top_ave) + ", DOES NOT QUALIFY FOR HONORS STUDY! Try Masters by course work."
    server.register_function(determineHonours)

    def isExistingStudent(id):
        results = db.queryDB("students", "id", id)
        if len(results) == 0:
            return False
        elif len(results) == 1:
            return True
    server.register_function(isExistingStudent)

    def getGrades(id):  # TODO: Gets grades for a particular student
        unit_list = []
        db_grades = db.getGrades(id)

    dev = True  # ! Developer mode for db management and testing ===============
    if dev:
        print("Developer mode active.")
        while True:
            choice = input("Choose function: ")
            if choice == "exit":
                break
            elif choice == "addUnit":
                param = input("param: ")
                db.addUnit(param)
            elif choice == "addStudent":
                param = input("param: ")
                db.addStudent(param)
    # ! End developer area =======================================================
    else:
        print("Server is running.")
        server.serve_forever()
