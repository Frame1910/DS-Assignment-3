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
        print("Generating database...")
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
        cursor.execute(
            "CREATE TABLE grades (id int PRIMARY KEY AUTO_INCREMENT, student_id varchar(8) NOT NULL, code varchar(6) NOT NULL, mark int NOT NULL)")
        return cursor

    def queryStudent(self, id):
        sql = "SELECT student_id FROM grades WHERE id=" + id
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def getGrades(self, id):  # Method to fetch a list of all grades for a particular student
        sql = 'SELECT * FROM grades WHERE id=' + id
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def addGrade(self, id, code, grade):  # * Method to add grade record to database SINGLE ENTRY
        sql = 'INSERT INTO grades (id, code, mark) VALUES (%s, %s, %s)'
        values = (id, code, grade)
        self.cursor.execute(sql, values)
        self.cnx.commit()
        print(self.cursor.rowcount, "records inserted.")

    def addGrades(self, person_details):  # * Method to add grade record to database BATCH ENTRY
        sql = 'INSERT INTO grades (id, code, mark) VALUES (%s, %s, %s)'
        values = []
        id = person_details[0]
        unit_list = person_details[1]
        for unit in unit_list:
            values.append((id, unit[0], unit[1]))

        self.cursor.executemany(sql, values)
        self.cnx.commit()
        print(self.cursor.rowcount, "records inserted.")

        self.cursor.execute(sql, values)
        self.cnx.commit()
        print(self.cursor.rowcount, "records inserted.")

    # Checks how many unit grades a given student has
    def checkUnitCount(self, user_id):
        self.cursor.execute(
            "SELECT * FROM grades WHERE id ='" + str(user_id) + "'")
        return len(cursor)

    def addNewUnits(self, person_details):
        pass


db = Database("root", "Letmein!1")
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # * Stage 1 Methods ===================================
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

    # * Stage 2 methods ===================================

    def isExistingStudent(id):
        results = db.queryStudent(id)
        if len(results) > 0:
            return True
        else:
            return False
    server.register_function(isExistingStudent)

    def getGrades(id):  # Gets grades for a particular student
        return db.getGrades(id)
    server.register_function(getGrades)

    def saveAll(person_details):  # Saves new student data to database
        db.addGrades(person_details)
    server.register_function(saveAll)

    dev = False
    inpt = input("Dev? ")
    if inpt == "y":
        dev = True  # ! Developer mode for db management and testing ===============
    if dev:
        print("Developer mode active.")
        while True:
            choice = input("Choose function: ")
            if choice == "exit":
                break
            elif choice == "addGrade":
                param1 = input("ID: ")
                param2 = input("Unit Code: ")
                param3 = input("Grade: ")
                db.addGrade(param1, param2, param3)
            elif choice == "getGrades":
                param = input("ID: ")
                grades = db.getGrades(param)
                print(grades)
            elif choice == "checkStudent":
                param = input("ID: ")
                exists = isExistingStudent(param)
                print(exists)

    # ! End developer area =======================================================
    else:
        print("Server is running.")
        server.serve_forever()
