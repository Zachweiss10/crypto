#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
import maya
blockchain = []
from project import blockchain

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
                                 str.encode(self.state), self.dataLength, str.encode(self.data))
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
        return unpackedData


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
