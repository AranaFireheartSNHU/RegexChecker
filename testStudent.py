#!/usr/bin/env python
__author__ = "Arana Fireheart"

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
            return returnString#, self.expectedResults[lastIndex], self.studentsResults[lastIndex])
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

testStudent = Student("Dummy")
testStudent.setGrades([10, ] * 32)
testStudent.setExpectedResults(["blah"] * 32)
testStudent.setStudentsResults(["boo"] * 32)

testIter = iter(testStudent)
# print(next(testIter))
# print(next(testIter))
# print(next(testIter))

for patternNumber, grade in enumerate(testIter):
    print(f"Pattern{patternNumber}: {grade}\n")

for patternNumber, studentTuple in enumerate(testStudent):
    grade, expected, generated = studentTuple
    print(f"Pattern{patternNumber}: {grade} Expected: {expected} Actual: {generated}\n")