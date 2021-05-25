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


# Checks for previous attempts the draft unit
# ! Does not work, need to clarify logic.
def checkAttempts(existing_units, draft_unit):
    previous_attempts = []
    for unit in existing_units:
        if unit[0] == draft_unit[0]:
            previous_attempts.append(unit)
    fails = 0
    for unit in previous_attempts:
        if unit[1] < 50:
            fails += 1
    if fails >= 2:
        print("You've failed",
              draft_unit[0], "too many times. You do not qualify for Honours.")
        return False


def validateUnitInput(existing_units, draft_unit):  # Validates new unit input
    # Checks draft unit for errors
    if draft_unit[1] < 0 or draft_unit[1] > 100:
        print("Invalid score. Try again.")
        return False
    code = draft_unit[0]
    if not code[0:3].isalpha() or not code[3:6].isnumeric():
        print("Unit code invalid. Try again.")
        return False
    return True


def enterUnits():
    # * unit_list = [ [Unit Code, Score], [Unit Code, Score], ...]
    unit_list = []
    while len(unit_list) < 30:
        print("Number of units entered:", str(len(unit_list)) + "/30")
        unit_result = input(
            "Please enter your unit information e.g. 'CSI3106, 75' or type exit:\n")
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
        # Unit validation function
        if not validateUnitInput(unit_list, unit_result):
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
