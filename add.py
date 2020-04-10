#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block
from parse import parse, itemIDS, blockList



BCHOC_FILE_PATH = "./blocParty"

def add(caseId, itemID):
    #need to hash parent
    global itemIDS
    parse()
    num = len(blockList)
    itemID = sum(itemID, [])
    parent = blockList[num-1]
    prevHash = parent.getHash()
    prevHash = prevHash.hexdigest()

    #check if command contains duplicate itemId's enter by user
    if len(itemID) !=len(set(itemID)):
        exit(666)


    print(itemIDS)
    #check if any of the itemIds have duplicates
    itemIDS += itemID
    if len(itemIDS) !=len(set(itemIDS)): 
        exit(666) 



    #append the block
    blockFile = open(BCHOC_FILE_PATH, 'ab') 
    for j in range(0, len(itemID)):
        currTime = datetime.datetime.now(datetime.timezone.utc)
        timestamp = currTime.timestamp()
        packedData = Block(prevHash=prevHash.encode(), timestamp=timestamp, state="CHECKEDIN", caseID=caseId.encode(), evidenceID= int(itemID[j]), dataLength=0, data="").packData()
        blockFile.write(packedData)
        print("Added item:",end=" ")
        print(itemID[j])
        print("  Status: CHECKEDIN")
        print("  Time of action: ",end="")
        print(currTime)
        num = len(blockList)
        #add to global list, create hash of recently added Block for next iteration
        parent = Block()
        parent.unpackData(packedData)
        print(parent.prevHash)
        blockList.append(parent)
        prevHash = parent.getHash()
        prevHash = prevHash.hexdigest()
    blockFile.close()

    return 0