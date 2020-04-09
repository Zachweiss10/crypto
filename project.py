#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from add import add
from Block import Block
from parse import *
blockList = []
from project import blockList

BCHOC_FILE_PATH = "./blocParty"

# Successful commands should exit with 0
def dieWithSuccess():
    exit(0)

# Unsuccessful commands should exit with non-zero
def dieWithError():
    print("error")
    exit(666)

# Checks if blockchain file exists
def checkExist():
    if(os.path.isfile(BCHOC_FILE_PATH)):
        return True
    else:
        return False

# Init command creates blockchain file with initial block if it
# doesn't already exist
def init():
    if(checkExist()):
        # Maybe add code to check the contents of the file to see that the info inside 
        # is actually the initial block
        blockFile = open(BCHOC_FILE_PATH, 'rb')
        data = blockFile.read()
        blockFile.close()
        block = Block()
        block.unpackData(data)
        print("Blockchain file found with INITIAL block.")
        dieWithSuccess()
    else:
        packedData = Block(prevHash=bytes(0x00), state="INITIAL", caseID=bytes(0x00), evidenceID=0, dataLength=14, data="Initial Block").packData()
        blockFile = open(BCHOC_FILE_PATH, 'wb')
        blockFile.write(packedData)
        blockFile.close()
        print("Blockchain file not found. Created INITIAL block.")
        dieWithSuccess()

#add command created n numbers of items for a specific caseID


def checkout():
    return

def log():
    return

def remove():
    return

def main():
    inputString = sys.argv
    if (inputString[1] == "init"):
        init()
    elif inputString[1] == "add":
        add(inputString)
    elif inputString[1] == "checkout":
        checkout()
    elif inputString[1] == "log":
        log()
    elif inputString[1] == "remove":
        remove()
    else:
        dieWithError()



if __name__ == '__main__':
    main()
