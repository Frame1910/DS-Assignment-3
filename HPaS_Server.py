import mysql.connector
import pyfiglet


def checkDBExistence():
    print("Checking for existing database...")
    cursor.execute("SHOW DATABASES")
    for database in cursor:
        print(database)
        if database[0] == "hpas_data":
            print("Existing database found!")
            return True
    print("No existing database found.")
    return False


# Print welcome banner for style points
welcome_banner = pyfiglet.figlet_format("HPaS Server")
print("\nWelcome to:\n", welcome_banner)

# Authentication of database server
while True:
    user_name = "root"  # ! input("Please enter database username:\n")
    password = "Letmein!1"  # ! input("Please enter database password:\n")
    try:
        db = mysql.connector.connect(  # ! Update for submission
            host="localhost",
            user=user_name,
            password=password
        )
        break
    except:
        print("\n*** Invalid credentials, make sure to use the credentials you used when setting up MySQL.***\n\nPlease try again...")

cursor = db.cursor()
db_exists = checkDBExistence()
print(db_exists)
if db_exists:
    print("\nReconnecting to existing database...")
else:
    print("\nCreating new database...")
    cursor.execute("CREATE DATABASE hpas_data")
db.connect(database="hpas_data")
print("Connected.")
