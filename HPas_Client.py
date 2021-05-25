# Darren Meiring (10496696)
# Byron Gregoriadis (10497015)
import xmlrpc.client


def checkFails(units):  # Checks how many failing marks have been entered and returns a Boolean value based on result
    fails = 0
    for unit in units:
        if unit[1] < 50:
            fails += 1
    if fails > 6:
        return False
    else:
        return True


def enterUnits():
    # * unit_list = [ [Unit Code, Score], [Unit Code, Score], ...]
    unit_list = []
    while len(unit_list) < 30:
        print("Number of units entered:", str(len(unit_list)) + "/30")
        unit_result = input(
            "Please enter your unit information e.g. 'CSI3106, 75' or type exit:\n")
        # TODO: Add validation for unit codes/scores? Seems like it would be difficult to do with strings.
        if unit_result == "exit":
            if len(unit_list) < 12:
                print("Minimum of 12 units is required.")
                continue
            break
        # Remove spaces and split unit code/score input into "code,score" for pre-processing
        unit_result = unit_result.replace(" ", "")
        unit_result = unit_result.split(",")
        # Convert score into integer for easier comparison later on
        try:
            unit_result[1] = int(unit_result[1])
        except ValueError:
            print("Please enter a number between 0 and 100. Try again.")
            continue
        if 0 > unit_result[1] > 100:  # Check if score is between 0 and 100
            print("Invalid score input, try again.")
            continue
        unit_list.append(unit_result)
    if checkFails(unit_list):
        return unit_list
    else:
        print("You have failed more than 6 of your units, you do not qualify for Honours.")
        exit()


print("Welcome to the Honours Pre-assessment System (HPaS)")
try:
    s = xmlrpc.client.ServerProxy('http://localhost:8000')
    print("Connected to server.")
except:
    print("Could not connect to server.")

person_id = input("Please enter your ID: ")
# * person_details is a 2-dimensional array which stores an ID in index 0, with index 1 containing another array; unit_list
# * person_details: [ ID, unit_list ]
person_details = []
person_details.append(person_id)
unit_grades = enterUnits()
# * At this point, the user has a valid ID, and has entered all units correctly
person_details.append(unit_grades)

s.displayScores(person_details)  # Prints scores on server's console
print("Course Average:", s.calculateGlobalAve(person_details))
print("Top 12 Scores:", s.twelveHighest(person_details))
print("Top 12 Average:", s.calculateTopTwelveAves(person_details))
print("Honours:", s.determineHonours(person_details))
