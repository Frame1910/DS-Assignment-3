# Darren Meiring (10496696)
# Byron Gregoriadis (10497015)
import xmlrpc.client


def yesNoInput(msg):
    while True:
        choice = input(msg + " (y/n): ")
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Please enter y or n. Try again.")


def checkFails(units):  # Checks how many failing marks have been entered and returns a Boolean value based on result
    fails = 0
    for unit in units:
        if unit[1] < 50:
            fails += 1
    if fails > 6:
        return False
    else:
        return True


# Checks that there are less than 4 attempts of a particular unit
def attempts(existing_units, draft_unit):
    previous_attempts = []
    for unit in existing_units:
        if unit[0] == draft_unit[0]:
            previous_attempts.append(unit[0])
    return len(previous_attempts)


# Checks how many fails there are for a particular unit
def existingFails(existing_units, draft_unit):
    fails = 0
    for unit in existing_units:
        if unit[0] == draft_unit[0] and unit[1] < 50:
            fails += 1
    return fails


def validateID():  # * Validates that an entered ID is 8 characters long and is numeric. However, it keeps it as a string to keep trailing zeros
    while True:
        id = input("Please enter your ID: ")
        if len(id) == 8 and id.isnumeric():
            return id
        else:
            print("Invalid ID. Try again.")


def validateUnitInput(existing_units, draft_unit):  # Validates new unit input
    # Convert score into integer for easier comparison later on
    try:
        draft_unit[1] = int(draft_unit[1])
        if draft_unit[1] < 0 or draft_unit[1] > 100:
            raise(ValueError)
    except ValueError:
        print("Please enter a number between 0 and 100. Try again.")
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
        # Unit validation function
        if validateUnitInput(unit_list, unit_result):
            unit_result[1] = int(unit_result[1])
            unit_attempts = attempts(unit_list, unit_result)
            existing_fails = existingFails(unit_list, unit_result)
            if unit_attempts == 3:
                print("You already have three marks entered for this unit")
                continue
            elif unit_attempts == 2 and existing_fails == 2:
                if unit_result[1] < 50:
                    print(
                        "You've failed", unit_result[0], "three times, you do not qualify for Honours")
                    exit()
            elif unit_attempts == 1 and existing_fails == 0 or unit_attempts == 2 and existing_fails == 1:
                if unit_result[1] >= 50:
                    print("You cannot pass one unit more than once.")
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

# * person_details is a 2-dimensional array which stores an ID in index 0, with index 1 containing another array; unit_list
# * person_details: [ ID, unit_list ]
person_details = []

person_id = validateID()
if s.isExistingStudent(person_id):
    choice = yesNoInput(
        "Would you like to use your existing data for the honours pre-assessment?")
    if choice:
        unit_grades = s.getGrades(person_id)
    else:
        unit_grades = enterUnits()
        save = yesNoInput(
            "Would you like to save these results in the HPaS Database?")
else:
    unit_grades = enterUnits()
    save = yesNoInput(
        "Would you like to save these results in the HPaS Database?")

# * At this point, the user has a valid ID, and has entered all units correctly
person_details.append(person_id)
person_details.append(unit_grades)
if save:
    s.saveAll(person_details)
s.determineHonours(person_details)
