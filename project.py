#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
import argparse
import maya
from add import add
from Block import Block
from parse import parse, itemIDS, blockList
from checkout import checkout


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
        print("Blockchain file not found. Created INITIAL block." + chr(7))
        dieWithSuccess()

#add command created n numbers of items for a specific caseID




def log():
    return

def remove():
    return

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", action="store", type=str)
    ap.add_argument("-c", required=False, type=str)
    ap.add_argument("-i", required=False, action="append", nargs="+", type=int)
    ap.add_argument("-r", required=False, type=bool)
    ap.add_argument("-n", required=False, type=int)
    ap.add_argument("-o", required=False, type=str)

    args = ap.parse_args()
    command = args.command
    caseID = args.c
    evidenceID = args.i
    reverse = args.r
    listNum = args.n
    identification = args.o

    if (command == "init"):
        init()
    elif command == "add":
        if not os.path.exists("./blocParty"):
            init()
        add(caseID, evidenceID)
    elif command == "checkout":
        checkout(evidenceID)
    elif command == "log":
        log(reverse, listNum)
    elif command == "remove":
        remove()
    elif command == "verify":
        if(checkExist()):
            returnList = parse()
            print("Initialblock is: prevHash-{0}, timeStamp-{1}, caseID-{2}, itemID-{3}, state-{4}, dataLength-{5}, dataString-{6}".format(returnList[0].prevHash, returnList[0].timestamp, returnList[0].caseID, returnList[0].evidenceID, returnList[0].state, returnList[0].dataLength, returnList[0].data))
        else:
            print("Transactions in blockchain: 0")
            print("State of blockchain: ERROR")
            print("Bad block: N/A")
            print("Blockchain file does not exist")
    else:
        dieWithError()



if __name__ == '__main__':
    main()
