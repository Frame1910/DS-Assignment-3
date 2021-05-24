import mysql.connector
import pyfiglet

user_name = "root"  # ! input("Please enter database username:\n")
password = "Letmein!1"  # ! input("Please enter database password:\n")


class Evaluator():
    def __init__(self, user, pwd):
        self.user_name = user
        self.pwd = pwd

        if self.checkDBExistence() != True:
            print("Error creating database, exiting...")
            exit()

    def checkDBExistence(self):
        # Authentication of database server
        while True:
            user_name = "root"  # ! input("Please enter database username:\n")
            # ! input("Please enter database password:\n")
            password = "Letmein!1"
            try:
                db = mysql.connector.connect(  # ! Update for submission
                    host="localhost",
                    user=self.user_name,
                    password=self.pwd
                )
                cursor = db.cursor()
                break
            except:
                print("\n*** Invalid credentials, make sure to use the credentials you used when setting up MySQL.***\n\nPlease try again...")
        print("Checking for existing database...")
        cursor.execute("SHOW DATABASES")
        for database in cursor:
            if database[0] == "hpas_data":
                print("Existing database found!")
                db.close()
                return True
        print("No existing database found.\nAttemping to create one...")
        try:
            cursor.execute("CREATE DATABASE hpas_data")
            db.close()
        except:
            return False
        return True

    def DBConnect(self):
        db = mysql.connector.connect(  # ! Update for submission
            host="localhost",
            user=self.user_name,
            password=self.pwd,
            database="hpas_data"
        )
        print("Connected to HPaS Database.")


# Print welcome banner for style points
welcome_banner = pyfiglet.figlet_format("HPaS Server")
print("\nWelcome to:\n", welcome_banner)
