# Mock data variables
mock_unit_list = [
    ["CSP0000", 40],
    ["CSP0000", 40],
    ["CSP0000", 40],
    ["CSP0000", 40],
    ["CSP0001", 40],
    ["CSP0002", 80],
    ["CSP0003", 80],
    ["CSP0004", 80],
    ["CSP0005", 80],
    ["CSP0006", 80],
    ["CSP0007", 80],
    ["CSP0008", 80],
    ["CSP0009", 80],
    ["CSP0010", 80],
    ["CSP0011", 80],
    ["CSP0011", 80],
    ["CSP0011", 80],
    ["CSP0011", 80]
]
mock_person = [
    "10496696",
    mock_unit_list
]


class Evaluator():
    def displayScores(self, person_info):
        units = person_info[1]
        for unit in units:
            print(unit[0], unit[1])

    def calculateGlobalAve(self, person_info):
        units = person_info[1]
        total = 0
        for unit in units:
            total += unit[1]
        return round(total/len(units), 2)

    def twelveHighest(self, person_info):
        scores_array = []
        units = person_info[1]
        for unit in units:
            scores_array.append(unit[1])
        scores_array.sort(reverse=True)
        return scores_array[0:12]

    def calculateTopTwelveAves(self, person_info):
        arr = self.twelveHighest(person_info)
        total = sum(arr)
        return round(total/len(arr), 2)

    def determineHonours(self, person_info):
        global_ave = self.calculateGlobalAve(person_info)
        top_ave = self.calculateTopTwelveAves(person_info)
        if global_ave >= 70:
            return person_info[0] + ", " + str(global_ave) + ", QUALIFIED FOR HONOURS STUDY!"
        elif global_ave < 70 and top_ave >= 80:
            return person_info[0] + ", " + str(global_ave) + ", " + str(top_ave) + ", MAY HAVE GOOD CHANCE! Need further assessment!"
        elif global_ave < 70 and 70 <= top_ave <= 80:
            return person_info[0] + ", " + str(global_ave) + ", " + str(top_ave) + ", MAY HAVE A CHANCE! Must be carefully reassessed and get the coordinator’s special permission!"
        elif global_ave < 70 and top_ave < 70:
            return person_info[0] + ", " + str(global_ave) + ", " + str(top_ave) + ", DOES NOT QUALIFY FOR HONORS STUDY! Try Masters by course work."

    def sendResult(self):
        pass


eval = Evaluator()
eval.displayScores(mock_person)
print("Average:", eval.calculateGlobalAve(mock_person))
for item in eval.twelveHighest(mock_person):
    print(item)

print(eval.calculateTopTwelveAves(mock_person))
print(eval.determineHonours(mock_person))
