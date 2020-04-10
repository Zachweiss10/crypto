import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block
blockList = []
itemIDS = []
theCaseID = ""

BCHOC_FILE_PATH = os.environ['BCHOC_FILE_PATH']
#BCHOC_FILE_PATH = "./blocParty"

def parse():
    global theCaseID
    parseFile = open(BCHOC_FILE_PATH, 'rb')
    currPos = 0
    blockEnd = 0
    data = parseFile.read()
    datax = data
    while(currPos < len(data)):
        # Check if first block is Initial
        if(data[currPos:currPos+20] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
            readBlock = Block()
            readBlock.unpackData(datax)
            #set previous hash to None
            pHash = None
            print("initial block found in parser")
            print("pHash is: {0}".format(pHash))
            currPos += 24

            # set timeStamp
            timeStamp = data[currPos:currPos + 8]
            print("Timestamp is: {0}".format(timeStamp))
            currPos += 8

            # set caseID to none
            caseID = None
            print("caseID is: {0}".format(caseID))
            currPos += 16

            # set itemID to None
            itemID = None
            print("itemID is: {0}".format(itemID))
            currPos += 4

            # set state
            state = data[currPos:currPos + 11].decode('ascii')
            print("State is: {0}".format(state))
            currPos += 12

            #set dataLength
            dataLength = int.from_bytes(data[currPos:currPos + 4], "little", signed=False)
            print("data length is: {0}".format(dataLength))
            currPos += 4

            #set dataString
            dataString = data[currPos:currPos + dataLength].decode('ascii')
            print("dataString is: {0}".format(dataString))

            # keep track of end of block
            currPos += dataLength
            print("End of block at: {0}".format(currPos))

            thisBlock = Block(pHash, timeStamp, caseID, itemID, state, dataLength, dataString)
            blockList.append(readBlock)
            datax = datax[(68 + int(readBlock.dataLength)):]

        else:
            readBlock = Block()
            readBlock.unpackData(datax)
            #set previous hash
            pHash = data[currPos:currPos + 20].decode('ascii')
            print("next block found in parser")
            print("pHash is: {0}".format(pHash))
            currPos += 24

            # set timeStamp
            timeStamp = data[currPos:currPos + 8]
            print("Timestamp is: {0}".format(timeStamp))
            currPos += 8

            # set caseID
            caseID = int.from_bytes(data[currPos:currPos + 16], "little", signed=False)
            print("caseID is: {0}".format(caseID))
            theCaseID = str(caseID)
            currPos += 16

            # set itemID
            itemID = int.from_bytes(data[currPos:currPos + 4], "little", signed=False)
            itemIDS.append(itemID)
            print("itemID is: {0}".format(itemID))
            currPos += 4

            # set state
            state = data[currPos:currPos + 11].decode('ascii')
            print("State is: {0}".format(state))
            currPos += 12

            #set dataLength
            dataLength = int.from_bytes(data[currPos:currPos + 4], "little", signed=False)
            print("data length is: {0}".format(dataLength))
            currPos += 4

            #set dataString
            dataString = data[currPos:currPos + dataLength].decode('ascii')
            print("dataString is: {0}".format(dataString))
            # keep track of end of block
            currPos += dataLength
            print("End of block at: {0}".format(currPos))

            blockList.append(readBlock)
            datax = datax[(68 + int(readBlock.dataLength)):]

    parseFile.close()
    return blockList, itemIDS, theCaseID