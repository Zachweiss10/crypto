#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
import argparse
from add import add
from Block import Block, BCHOC_FILE_PATH
from parse import parse, itemIDS, blockList, count
from checkout import checkout
from checkin import checkin
from remove import remove
from verify import verify
import re
import uuid


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
        try:
            block.unpackData(data)
        except:
            print("invalid block")
            dieWithError()
        print("Blockchain file found with INITIAL block.")
        dieWithSuccess()
    else:
        packedData = Block(prevHash=bytes(0x00), state="INITIAL", caseID="00000000-0000-0000-0000-000000000000", evidenceID=0, dataLength=14, data="Initial block").packData()
        blockFile = open(BCHOC_FILE_PATH, 'wb')
        blockFile.write(packedData)
        blockFile.close()
        print("Blockchain file not found. Created INITIAL block.")
        dieWithSuccess()

#add command created n numbers of items for a specific caseID



def log(reverse, numberOfEntries, itemID=None, caseID=None):
    parse()
    caseList = []
    itemList = []
    printList = []

    if blockList == None:
        print("there are no blocks to be printed!")
        dieWithError()

    if caseID != None:
        for block in blockList:
            if caseID == block.caseID:
                caseList.append(block)
    else:
        caseList = blockList

    if itemID != None:

        for item in itemID:
            for block in blockList:
                if item[0] == block.evidenceID:
                    itemList.append(block)
    else:
        itemList = blockList

    printList = [value for value in itemList if value in caseList]


    if numberOfEntries == None:
        numberOfEntries = len(printList)

    if numberOfEntries > len(printList):
        numberOfEntries = len(printList)

    if(reverse):
        for x in range(numberOfEntries -1, -1, -1):
            if printList[x].timestamp == 0:
                dt_iso = 0

            else:
                dt = datetime.datetime.fromtimestamp(printList[x].timestamp)
                dt_iso = dt.isoformat()
            print("Case: {c}".format(c=(printList[x].caseID) ) )
            print("Item: {i}".format(i=printList[x].evidenceID) )
            print("Action: {a}".format(a=printList[x].state.rstrip(' \t\r\n\0') ) )
            print("Time: {t}".format(t=dt_iso))
            print("")
    else:
        for x in range(numberOfEntries):
            if printList[x].timestamp == 0:
                dt_iso = 0

            else:
                dt = datetime.datetime.fromtimestamp(printList[x].timestamp)
                dt_iso = dt.isoformat()
            print("Case: {c}".format(c=(printList[x].caseID) ) )
            print("Item: {i}".format(i=printList[x].evidenceID) )
            print("Action: {a}".format(a=printList[x].state.rstrip(' \t\r\n\0') ) )
            print("Time: {t}".format(t=dt_iso))
            print("")
    return

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", action="store", type=str)
    ap.add_argument("-c", required=False, type=str)
    ap.add_argument("-i", required=False, action="append", nargs="+", type=int)
    ap.add_argument("-r", "--reverse", action="store_true")
    ap.add_argument("-n", required=False, type=int)
    ap.add_argument("-o", required=False, type=str)
    ap.add_argument("-y", "--why", required=False, type=str)

    args = ap.parse_args()
    command = args.command
    caseID = args.c
    evidenceID = args.i
    reverse = args.reverse
    listNum = args.n
    owner = args.o
    reason = args.why

    if (command == "init"):
        init()
    elif command == "add":
        if not os.path.exists(BCHOC_FILE_PATH):
            init()
        add(caseID, evidenceID)
    elif command == "checkout":
        checkout(evidenceID)
    elif command == "checkin":
        checkin(evidenceID)
    elif command == "log":
        log(reverse, listNum, evidenceID, caseID)
    elif command == "remove":
        remove(evidenceID, reason, owner)
    elif command == "verify":
        if(checkExist()):
            try:
                returnList = parse()
            except:
                print("invalid block after initial")
                dieWithError()
            verify()
            #causes error
            #print("Initialblock is: prevHash-{0}, timeStamp-{1}, caseID-{2}, itemID-{3}, state-{4}, dataLength-{5}, dataString-{6}".format(returnList[0].prevHash, returnList[0].timestamp, returnList[0].caseID, returnList[0].evidenceID, returnList[0].state, returnList[0].dataLength, returnList[0].data))
        else:
            print("Transactions in blockchain: 0")
            print("State of blockchain: ERROR")
            print("Bad block: N/A")
            print("Blockchain file does not exist")
    else:
        dieWithError()



if __name__ == '__main__':
    main()