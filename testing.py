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


unit_list = [
    ["SCI1125", 82],
    ["CSP1150", 78],
    ["MAT1252", 80],
    ["CSI1241", 85],
    ["CSG1105", 75],
    ["CSI1101", 70],
    ["ENS1161", 90],
    ["CSG1207", 87],
    ["CSP2348", 80],
    ["CSP2104", 77],
    ["CSG2341", 82],
    ["CSG2344", 80],
    ["CSI2312", 35],
    ["CSP3341", 40],
    ["CSI2312", 27]
]
unit_result = ["CSI2312", 40]


if validateUnitInput(unit_list, unit_result):
    unit_attempts = attempts(unit_list, unit_result)
    existing_fails = existingFails(unit_list, unit_result)
    if unit_attempts == 3:
        print("You already have three marks entered for this unit")
    elif unit_attempts == 2 and existing_fails == 2:
        if unit_result[1] < 50:
            print(
                "You've failed", unit_result[0], "three times, you do not qualify for Honours")
            exit()
    elif unit_attempts == 1 and existing_fails == 0 or unit_attempts == 2 and existing_fails == 1:
        if unit_result[1] >= 50:
            print("You cannot pass one unit more than once.")
