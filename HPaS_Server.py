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


class Database():  # Goal of the Database class is to provide an interface for server-1 to interact with the MySQL database server (server-2)
    # Goal of the constructor is to make sure a useable database is ready for use as well provide the rest of the class with a cursor object to execute queries
    def __init__(self, user, pwd, host="localhost", db="student_records"):
        try:  # Try to access the database, if no connection can be established, create the database
            self.cnx = mysql.connector.connect(
                user=user,
                password=pwd,
                host=host,
                database=db
            )
            self.cursor = self.cnx.cursor()
        except ProgrammingError:
            self.cursor = self.generateDatabase(user, pwd)

    # Generates a new student_records database from scratch and returns a db cursor to execute queries
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
            "CREATE TABLE grades (id int PRIMARY KEY AUTO_INCREMENT, student_id varchar(8) NOT NULL, code varchar(7) NOT NULL, mark int NOT NULL)")
        return cursor  # Cursor is used to execute SQL code throughout the class methods

    # Finds all references of a student ID in the database.
    def queryStudent(self, id):
        sql = "SELECT student_id FROM grades WHERE student_id=" + id
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def getGrades(self, id):  # Fetches a list of all grades for a particular student
        sql = 'SELECT code, mark FROM grades WHERE student_id=' + id
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def addGrades(self, person_details):  # Add grade record to database
        sql = 'INSERT INTO grades (student_id, code, mark) VALUES (%s, %s, %s)'
        values = []
        id = person_details[0]
        unit_list = person_details[1]
        for unit in unit_list:
            values.append((id, unit[0], unit[1]))
        self.cursor.executemany(sql, values)
        self.cnx.commit()
        print(self.cursor.rowcount, "records inserted.")

    # Delete a batch of grade records based on the student number
    def deleteStudentData(self, student_id):
        sql = "DELETE FROM grades WHERE student_id=" + student_id
        self.cursor.execute(sql)
        self.cnx.commit()
        print(self.cursor.rowcount, "record(s) deleted")


db = Database("root", "Letmein!1")  # Instantiate Database interface object
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Stage 1 Methods =========================================================================================================
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

    # Stage 2 methods ============================================================================================================================================

    # Checks if a student ID is already present in the database
    def isExistingStudent(id):
        results = db.queryStudent(id)
        if len(results) > 0:
            return True
        else:
            return False
    server.register_function(isExistingStudent)

    def getGrades(id):  # Gets grades for a particular student
        grades = db.getGrades(id)
        return grades
    server.register_function(getGrades)

    def saveAll(person_details):  # Saves new student data to database
        old = db.getGrades(person_details[0])
        if len(old) > 0:  # If old data is in the database for a particular student, delete it and add the new data
            db.deleteStudentData(person_details[0])
        db.addGrades(person_details)
    server.register_function(saveAll)

    dev = False
    inpt = input("Developer mode? (y/n)")
    if inpt == "y":
        dev = True  # ! Developer mode for database management and testing ONLY ===============
    if dev:
        print("Developer mode active.")
        while True:
            choice = input("Choose function: ")
            if choice == "exit":
                break
            elif choice == "getGrades":
                param = input("ID: ")
                grades = db.getGrades(param)
                print(grades)
            elif choice == "checkStudent":
                param = input("ID: ")
                exists = isExistingStudent(param)
                print(exists)
            elif choice == "honours":
                student_id = input("ID: ")
                param = [student_id, db.getGrades(student_id)]
                result = determineHonours(param)
                print(result)
            elif choice == "save":
                param = ["10496696", [
                        ["SCI1125", 96],
                        ["CSP1150", 92],
                        ["MAT1252", 92],
                        ["CSI1241", 95],
                        ["CSG1105", 86],
                        ["CSI1101", 78],
                        ["ENS1161", 94],
                        ["CSG1207", 91],
                        ["CSP2348", 86],
                        ["CSP2104", 88],
                        ["CSG2341", 90],
                        ["CSG2344", 86],
                        ["CSI3344", 76],
                        ["CSP3341", 78],
                        ["CSP2108", 75],
                        ["CSI2312", 72]]]
                db.addGrades(param)
            elif choice == "del":
                param = input("ID: ")
                db.deleteStudentData(param)

    # ! End developer area =======================================================
    else:
        print("Server is running.")
        server.serve_forever()
