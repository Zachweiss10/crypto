#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block
from parse import parse

BCHOC_FILE_PATH = "./blocParty"

def add(inputString):
    #Store case id, and (multiple) itemId
    #Ensure input errors end with a dieWithError()
    itemID = []
    if inputString[2] != "-c":
        dieWithError()
    caseID = inputString[3]
    inputString = inputString[4:]
    numOfCaseItems = len(inputString)
    for i in range(0,numOfCaseItems):
        if i % 2 == 1:
            itemID.append(inputString[i])
        else:
            if inputString[i] != "-i":
                dieWithError() 
    #need to hash parent
    #create new block
    blockFile = open(BCHOC_FILE_PATH, 'ab') 
    for j in range(0, len(itemID)):
        currTime = datetime.datetime.now(datetime.timezone.utc)
        timestamp = currTime.timestamp()
        packedData = Block(prevHash=bytes(0x00), timestamp=timestamp, state="CHECKEDIN", caseID=bytes(0x00), evidenceID= int(itemID[j]), dataLength=0, data="").packData()
        blockFile.write(packedData)
        print("Added item:",end=" ")
        print(itemID[j])
        print("  Status: CHECKEDIN")
        print("  Time of action: ",end="")
        print(currTime)

    blockFile.close()

    return 0