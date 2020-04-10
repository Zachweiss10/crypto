#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block
from parse import parse, itemIDS, blockList, theCaseID

BCHOC_FILE_PATH = os.environ['BCHOC_FILE_PATH'].strip()

def checkout(evidenceIDList):
    parse()
    maxTime = 0
    recentBlock = None

    #verify input
    if evidenceIDList == None:
        print("no evidence id provided!")
        dieWithError()

    for evidenceID in evidenceIDList:
        for block in blockList:
            if evidenceID[0] == block.evidenceID:
                if block.timestamp > maxTime:
                    maxTime = max(maxTime, block.timestamp)
                    recentBlock = block

        #if the evidenceID doesn't exist
        if recentBlock == None:
            print("no block exists with that evidence id!")
            dieWithError()

        tempState = "".join(e for e in recentBlock.state if e.isalnum())
        if tempState == "CHECKEDIN":
            pHash = blockList[-1].getHash()
            newBlock = Block(prevHash=pHash, caseID=recentBlock.caseID, evidenceID=evidenceID[0], state="CHECKEDOUT", dataLength=0, data="" )
            data = newBlock.packData()
            blockFile = open(BCHOC_FILE_PATH, 'ab')
            blockFile.write(data)
            blockFile.close()
            blockList.append(newBlock)
        else:
            print("block must be checkedin to be checked out!")
            dieWithError()
    return