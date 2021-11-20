#!/usr/bin/env python
__author__ = "Arana Fireheart"

from os import walk
from os.path import exists, join
import re
from datetime import datetime
from time import strftime

completedKey = "61239064"
attemptedKey = "71230875"
keyFilename = ".keyfile"
startingFolder = "/Users/arana/Library/Mobile Documents/com~apple~CloudDocs/SNHU/CS238/Spring 21/RegEx Assignments"
testStringsFilename = "testStrings.txt"
assignmentFilename = "regexpatterns.txt"
resultsFilename = "results.txt"
masterFilename = "allResults.txt"
totalNumberOfPatterns = 32

students = {}

class Student(object):
    def __init__(self, incomingName):
        self.name = incomingName
        self.grades = []
        self.expectedResults = []
        self.studentsResults = []
        self.isCompleted = False

    def __iter__(self):
        self.gradeIndex = 0
        return self

    def __next__(self):
        if self.gradeIndex < len(self.grades):
            lastIndex = self.gradeIndex
            self.gradeIndex += 1
            returnString = self.grades[lastIndex], self.expectedResults[lastIndex], self.studentsResults[lastIndex]
            return (self.grades[lastIndex], self.expectedResults[lastIndex], self.studentsResults[lastIndex])
        else:
            raise StopIteration()

    def setName(self, newName):
        self.name = newName

    def getName(self):
        return self.name

    def setGrades(self, newGrade):
        self.grades = newGrade

    def getGrades(self):
        return self.grades

    def setExpectedResults(self, newExpectedResults):
        self.expectedResults = newExpectedResults

    def getExpectedResults(self):
        return self.expectedResults

    def setStudentsResults(self, newStudentResults):
        self.studentsResults = newStudentResults

    def getStudentsResults(self):
        return self.studentsResults

    def setCompleted(self, isCompleted):
        self.isCompleted = isCompleted

    def getCompleted(self):
        return self.isCompleted


def getTestStrings(fileName):
    currentAssignment = -1
    testStrings = {}
    testsList = []
    with open(fileName, 'r') as testInput:
        for string in testInput.readlines():
            testString = string.strip().split('\t')
            if int(testString[0]) != currentAssignment:  # Found beginning of new assignment.
                if currentAssignment >= 0:
                    testStrings[currentAssignment] = testsList  # Stash the last list
                currentAssignment = int(testString[0])
                testsList = [testString[1:]]
            else:
                if len(testsList) != 0:         # Not the first entry in list
                    testsList.append(testString[1:])
        testStrings[currentAssignment] = testsList  # Stash the last one before leaving

        return testStrings

def keyCheck(inputFile):
    with open(inputFile, 'r')as keyInput:
        if keyInput.readline().strip() == completedKey:
            completed = True
        elif keyInput.readline().strip() == attemptedKey:
            completed = False
        grade = keyInput.readline().strip()
        return completed, grade


def keyGen(inputFile, isCompleted):
    with open(inputFile, 'w')as keyOutput:
            if isCompleted:
                keyOutput.write(f"{completedKey}\n")
            else:
                keyOutput.write(f"{attemptedKey}\n")


def buildStudentData():
    for root, dirs, files in walk(startingFolder):
        for studentFolder in dirs:
            keyFullFilename = join(startingFolder, studentFolder, keyFilename)
            try:
                isCompleted, grade = keyCheck(keyFullFilename)
            except FileNotFoundError:
                isCompleted = False
                grade = 0
            newStudent = Student(studentFolder)
            newStudent.setName(studentFolder)
            newStudent.setGrades(grade)
            newStudent.setCompleted(isCompleted)
            students[studentFolder] = newStudent


def checkAssignment(studentName, testStrings):
    assignmentFileFull = join(startingFolder, studentName, assignmentFilename)
    studentGrades = []
    resultsExpectedForGrades = []
    resultsGeneratedForGrades = []
    try:
        with open(assignmentFileFull, 'r') as assignment:
            for lineNumber, regexPattern in enumerate(assignment.readlines()):
                regexPattern = regexPattern.strip()
                assignmentNumber = lineNumber
                if 0 <= assignmentNumber <= 6:
                    currentTestStrings = testStrings[assignmentNumber]
                    for testString in currentTestStrings:
                        if len(testString) == 2:
                            mode, testString = testString
                            if mode == "Match":
                                resultsExpectedForGrades.append(str(testString))
                            else:
                                resultsExpectedForGrades.append("")
                        elif len(testString) == 3:
                            mode, testString, capturedData = testString
                            resultsExpectedForGrades.append(str(capturedData))
                        else:
                            resultsExpectedForGrades.append("")
                            raise ValueError
                        if len(regexPattern) > 0:
                            try:
                                if mode == "Match":
                                    matchObj = re.match(regexPattern, testString)
                                    if matchObj is not None:
                                        resultsGeneratedForGrades.append(str(matchObj))
                                    else:
                                        resultsGeneratedForGrades.append("None")
                                    if matchObj:
                                        if matchObj.string == testString:
                                            studentGrades.append(10)
                                    else:
                                        studentGrades.append(0)
                                elif mode == "Capture":
                                    matchObj = re.findall(regexPattern, testString)
                                    if matchObj is not None:
                                        resultsGeneratedForGrades.append(str(matchObj))
                                    else:
                                        resultsGeneratedForGrades.append("None")
                                    if matchObj:
                                        if type(matchObj) is list:
                                            foundData = []
                                            if type(matchObj[0]) is tuple:
                                                [foundData.append(result) for stringList in matchObj for result in stringList]
                                            else:
                                                foundData.extend(matchObj)
                                            answers = capturedData.split()
                                            if len(answers) == len(foundData):
                                                for answer in answers:
                                                    if answer not in foundData:
                                                        studentGrades.append(0)
                                                        break
                                                studentGrades.append(10)
                                            else:
                                                studentGrades.append(0)
                                        elif capturedData in foundData:
                                            studentGrades.append(10)
                                        else:
                                            studentGrades.append(0)
                                    else:
                                        studentGrades.append(0)

                                elif mode == "CaptureSp":
                                    matchObj = re.findall(regexPattern, testString)
                                    if matchObj is not None and len(matchObj) > 0:
                                        resultsGeneratedForGrades.append(matchObj[0])
                                    else:
                                        resultsGeneratedForGrades.append("None")
                                    if matchObj:
                                        if type(capturedData) is str:
                                            if capturedData == matchObj[0]:
                                                studentGrades.append(10)
                                        else:
                                            studentGrades.append(0)
                                    else:
                                        studentGrades.append(0)

                                elif mode == "Skip":
                                    matchObj = re.match(regexPattern, testString)
                                    if matchObj is None:
                                        resultsGeneratedForGrades.append("None")
                                        studentGrades.append(10)
                                    else:
                                        resultsGeneratedForGrades.append(str(matchObj))
                                        studentGrades.append(0)

                                else:
                                    print(f"Error unknown mode: {mode}")
                            except re.error:
                                resultsGeneratedForGrades.append("re.error")
                                studentGrades.append(0)

        return studentGrades, resultsExpectedForGrades, resultsGeneratedForGrades
    except FileNotFoundError:
        return ([0,] * 32), (["",] * 32), (["",] * 32)


buildStudentData()
assignmentTestStrings = getTestStrings(testStringsFilename)
for studentName, studentData in students.items():
    studentGrades, expectedStrings, generatedStrings = checkAssignment(studentData.getName(), assignmentTestStrings)
    studentData.setCompleted(0 not in studentGrades)
    studentData.setGrades(studentGrades)
    studentData.setExpectedResults(expectedStrings)
    studentData.setStudentsResults(generatedStrings)
    pass

with open(join(startingFolder, masterFilename), 'a') as masterGradeFile:
    timeNow = datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
    seperator = '*' * 40
    masterGradeFile.write(f"{timeNow}\n")
    for studentName, student in students.items():
        resultsFileFull = join(startingFolder, student.getName(), resultsFilename)
        with open(resultsFileFull, 'w') as studentGradeReportFile:
            studentGradeReportFile.write(f"{timeNow}\n")
            runningTotal = 0
            for patternNumber, studentTuple in enumerate(student):
                grade, expected, generated = studentTuple
                studentGradeReportFile.write(f"Pattern{patternNumber + 1}: {grade} \tExpected: {expected}\tActual: {generated}\n")
                runningTotal += grade
            studentGradeReportFile.write(f"Average: {round(runningTotal / totalNumberOfPatterns, 1)}\n")
        masterGradeFile.write(f"Student: {studentName} Average: {round(runningTotal / totalNumberOfPatterns, 1)}\n")
    masterGradeFile.write(f"{seperator}\n\n")
pass
