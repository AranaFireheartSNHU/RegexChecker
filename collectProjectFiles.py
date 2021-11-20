#!/usr/bin/env python
__author__ = "Arana Fireheart"

from shutil import copyfile

import os

import time
from os import walk, path, stat, mkdir
from os.path import basename, join, exists, dirname

baseDirectory = "/home"
collectionDestination = "/home/arana.f/pythonProjects"

def copyAllFiles(sourceDirectory, destinationDirectory, fileExtension):
    for file in os.listdir(sourceDirectory):
        studentName = basename(dirname(sourceDirectory))
        studentFoldername = join(destinationDirectory, studentName)
        if not exists(studentFoldername):
            mkdir(studentFoldername)
        if file.endswith(fileExtension):
            print(f"Copying {join(sourceDirectory, file)} to {join(destinationDirectory, studentName, file)}")
            copyfile(join(sourceDirectory, file), join(destinationDirectory, studentName, file))

print("Getting Started!")
try:
    for root, dirs, files in walk(baseDirectory, topdown=True):
        for directory in dirs:
            if directory.lower() == "python":
                # print(f"Found Python folder in {basename(root)}")
                studentName = basename(root)
                copyAllFiles(join(root, directory), collectionDestination, ".py")
                # for name in files:
                #     if '/.' in root or '\.' in root or basename(root)[0] == '_':
                #         break
                #     else:
                #         if name.endswith(".py"):
                #             fullFilename = path.join(root, name)
                #             print(f"Found Python file in {fullFilename}")

except FileNotFoundError:
    print("File not found")
