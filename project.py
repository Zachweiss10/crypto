#!/usr/bin/env python3

import hashlib
import os.path
import sys
import datetime
import struct

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
                                 str.encode(self.state), 14, str.encode(self.data))
        return packedData


# Successful commands should exit with 0
def dieWithSuccess():
    exit(0)

# Unsuccessful commands should exit with non-zero
def dieWithError():
    exit(666)

# Checks if blockchain file exists
def checkExist():
    if(os.path.isfile(BCHOC_FILE_PATH)):
        return True
    else:
        return False

# Init command creates blockchain file with initial block if it
# doesn't already exist
if (sys.argv[1] == "init"):
    if(checkExist()):
        # Maybe add code to check the contents of the file to see that the info inside 
        # is actually the initial block
        print("Blockchain file found with INITIAL block.")
        dieWithSuccess()
    else:
        packedData = Block(prevHash=bytes(0x00), state="INITIAL", caseID=bytes(0x00), evidenceID=0, dataLength=14, data="Initial Block").packData()
        blockFile = open(BCHOC_FILE_PATH, 'wb')
        blockFile.write(packedData)
        blockFile.close()
        print("Blockchain file not found. Created INITIAL block.")
        dieWithSuccess()

else:
    dieWithError()
