
#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block, BCHOC_FILE_PATH
from parse import parse, itemIDS, blockList, theCaseID


def add(caseId, itemID):
    #need to hash parent
    global itemIDS
    global theCaseID
    parse()
    num = len(blockList)
    #check if item id's were passed
    if itemID == None:
        print("No itemIDs were passed")
        exit(666)
    itemID = sum(itemID, [])
    parent = blockList[num-1]
    prevHash = parent.getHash()
    prevHash = prevHash.hexdigest()

    #check if command contains duplicate itemId's enter by user
    if len(itemID) !=len(set(itemID)):
        print("ERROR: item duplicate")
        exit(666)


    x = set(itemID)
    y = set(itemIDS)
    z = x.intersection(y)
    print(z)
    #check if any of the itemIds have duplicates in the entire blockchain
    if len(z) != 0:
        print("ERROR: item is contained on the blockchain already") 
        exit(666) 
    #print(itemIDS)

    #check if caseID is blank
    if caseId == "":
        exit(666)

    #append the block
    blockFile = open(BCHOC_FILE_PATH, 'ab') 
    for j in range(0, len(itemID)):
        currTime = datetime.datetime.now(datetime.timezone.utc)
        timestamp = currTime.timestamp()
        packedData = Block(prevHash=prevHash.encode(), timestamp=timestamp, state="CHECKEDIN", caseID=caseId, evidenceID= int(itemID[j]), dataLength=0, data="").packData()
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