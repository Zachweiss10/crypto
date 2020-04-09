#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block
from parse import *

BCHOC_FILE_PATH = "./blocParty"

def add(caseId, itemID):
    #need to hash parent



    #check

    #append the block
    blockFile = open(BCHOC_FILE_PATH, 'ab') 
    for j in range(0, len(itemID)):
        currTime = datetime.datetime.now(datetime.timezone.utc)
        timestamp = currTime.timestamp()
        #print(type(val))
        #print(itemID)
        #print(type(itemID[j]))
        packedData = Block(prevHash=bytes(0x00), timestamp=timestamp, state="CHECKEDIN", caseID=bytes(0x00), evidenceID= int(itemID[j][0]), dataLength=0, data="").packData()
        blockFile.write(packedData)
        print("Added item:",end=" ")
        print(itemID[j])
        print("  Status: CHECKEDIN")
        print("  Time of action: ",end="")
        print(currTime)

    blockFile.close()

    return 0