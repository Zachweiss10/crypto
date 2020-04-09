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
from parse import *


BCHOC_FILE_PATH = "./blocParty"

class Block:

    def __init__(self,
                 prevHash=None,
                 timestamp=None,
                 caseID=None,
                 evidenceID=None,
                 state=None,
                 dataLength=None,
                 data=None ):
        self.prevHash = prevHash
        self.timestamp = timestamp
        self.caseID = caseID
        self.evidenceID = evidenceID
        self.state = state
        self.dataLength = dataLength
        self.data = data
        self._dataString = None
        self._hash = None

    def packData(self):
        if ( self.timestamp == None ):
            currTime = datetime.datetime.now(datetime.timezone.utc)
            self.timestamp = currTime.timestamp()
        if ( self.prevHash == None ):
            print( "No hash provided, the data couldn't be packed")
            return
        if ( self.caseID == None ):
            print( "No caseID provided, the data couldn't be packed")
            return
        if ( self.evidenceID == None ):
            print( "No evidenceID provided, the data couldn't be packed")
            return
        if ( self.state == None ):
            print( "No state provided, the data couldn't be packed")
            return
        if ( self.dataLength == None ):
            print( "No dataLength provided, the data couldn't be packed")
            return
        if ( self.data == None and self.dataLength != 0):
            print( "No data provided, the data couldn't be packed")
            return
        fmtString = "20s d 16s I 11s I {dataLength}s".format(dataLength=self.dataLength)
        packedData = struct.pack(fmtString, self.prevHash, self.timestamp, self.caseID, self.evidenceID,
                                 self.state.encode(), self.dataLength, self.data.encode())
        self._dataString = packedData
        self._hash = hashlib.sha1(packedData)
        return packedData

    def unpackData(self, data):
        unpackedData = struct.unpack_from("20s d 16s I 11s I", data, 0)
        self.prevHash = unpackedData[0]
        self.timestamp = unpackedData[1]
        self.caseID = unpackedData[2]
        self.evidenceID = unpackedData[3]
        self.state = (unpackedData[4]).decode()
        self.dataLength = unpackedData[5]
        unpackedData = struct.unpack_from("{dataLength}s".format(dataLength=self.dataLength), data, 68)
        self.data = (unpackedData[0]).decode()

        self._dataString = data[0:68 + self.dataLength]
        self._hash = hashlib.sha1(self._dataString)

    def getHash(self):
        if self._hash != None:
            return self._hash
        if self._dataString != None:
            return hashlib.sha1(self._dataString)

        print("Get hash was called on a block without data! Call pack or unpack data to generate a hash")
        return 0


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


def checkout(evidenceID):
    maxTime = 0
    recentBlock = None

    #verify input
    if evidenceID == None:
        dieWithError()

    for block in blockList:
        if evidenceID == block.evidenceID:
            if block.timestamp > maxTime:
                maxTime = max(maxTime, block.timestamp)
                recentBlock = block

    #if the evidenceID doesn't exist
    if recentBlock == None:
        dieWithError()

    if recentBlock.state == "CHECKEDIN":
        newBlock = Block()




    return

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
            dieWithError()
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
