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
startingFolder = "./"
testStringsFilename = "testStrings.txt"
assignmentFilename = "regexpatterns.txt"
resultsFilename = "results.txt"
totalNumberOfPatterns = 32


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


def checkAssignment(testStrings):
    assignmentFileFull = join(startingFolder, assignmentFilename)
    patternNumbers = []
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
                        patternNumbers.append(assignmentNumber + 1)
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
                                        resultsGeneratedForGrades.append(matchObj.string)
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
                                        if isinstance(matchObj, list):
                                            if len(matchObj) == 0:
                                                resultsGeneratedForGrades.append("None")
                                            elif len(matchObj) == 1:
                                                if isinstance(matchObj[0], str):
                                                    resultsGeneratedForGrades.append(matchObj[0])
                                                elif isinstance(matchObj[0], tuple):
                                                    combinedString = ""
                                                    for item in matchObj[0]:
                                                        if item != "":
                                                            combinedString += item + ' '
                                                    resultsGeneratedForGrades.append(combinedString.strip())
                                                else:
                                                    resultsGeneratedForGrades.append("splat")
                                    else:
                                        resultsGeneratedForGrades.append("None")
                                    if matchObj:
                                        if type(matchObj) is list:
                                            foundData = []
                                            if type(matchObj[0]) is tuple:
                                                [foundData.append(result) for stringList in matchObj for result in stringList]
                                            else:
                                                foundData.extend(matchObj)
                                            if '' in foundData:
                                                del foundData[foundData.index('')]
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
                                        resultsGeneratedForGrades.append(matchObj.string)
                                        studentGrades.append(0)

                                else:
                                    print(f"Error unknown mode: {mode}")
                            except re.error:
                                resultsGeneratedForGrades.append("re.error")
                                studentGrades.append(0)

        return patternNumbers, studentGrades, resultsExpectedForGrades, resultsGeneratedForGrades
    except FileNotFoundError:
        return ([0,] * 32), (["",] * 32), (["",] * 32)



assignmentTestStrings = getTestStrings(testStringsFilename)
patternNumber, studentGrade, expectedStrings, generatedStrings = checkAssignment(assignmentTestStrings)
for resultNumber in range(0, len(studentGrade)):
    print(f"Pattern: {patternNumber[resultNumber]} Grade: {studentGrade[resultNumber]} Expected: {expectedStrings[resultNumber]} Got: {generatedStrings[resultNumber]}")
pass
