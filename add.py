#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block
from parse import parse, itemIDS, blockList, theCaseID


BCHOC_FILE_PATH = os.environ['BCHOC_FILE_PATH']
#BCHOC_FILE_PATH = "./"blocParty

def add(caseId, itemID):
    #need to hash parent
    global itemIDS
    global theCaseID
    parse()
    num = len(blockList)
    itemID = sum(itemID, [])
    parent = blockList[num-1]
    prevHash = parent.getHash()
    prevHash = prevHash.hexdigest()


    #check if caseID is the same as the stored item id's case
        #strip excess null bytes
    '''caseID_str = blockList[num-1].caseID.decode()
    if num>1:
        if caseID_str != caseId:
            print(caseID_str)
            print(caseId)
            print("ERROR: caseIDs don't match")
            exit(666)'''

    #check if command contains duplicate itemId's enter by user
    if len(itemID) !=len(set(itemID)):
        print("ERROR: item duplicate")
        exit(0)


    #check if any of the itemIds have duplicates in the entire blockchain
    itemIDS += itemID
    if len(itemIDS) !=len(set(itemIDS)):
        print("ERROR: item is contained on the blockchain already") 
        exit(666) 
    #print(itemIDS)


    #append the block
    blockFile = open(BCHOC_FILE_PATH, 'ab') 
    for j in range(0, len(itemID)):
        currTime = datetime.datetime.now(datetime.timezone.utc)
        timestamp = currTime.timestamp()
        packedData = Block(prevHash=prevHash.encode(), timestamp=timestamp, state="CHECKEDIN", caseID=caseId.encode(), evidenceID= int(itemID[j]), dataLength=0, data="").packData()
        blockFile.write(packedData)
        print("Case: ",end="")
        print(caseId)
        print("Added item:",end=" ")
        print(itemID[j])
        print("  Status: CHECKEDIN")
        print("  Time of action: ",end="")
        print(currTime)
        num = len(blockList)
        #add to global list, create hash of recently added Block for next iteration
        parent = Block()
        parent.unpackData(packedData)
        blockList.append(parent)
        prevHash = parent.getHash()
        prevHash = prevHash.hexdigest()
    blockFile.close()

    return 0