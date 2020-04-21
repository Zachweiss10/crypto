#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block, BCHOC_FILE_PATH
from parse import parse, itemIDS, blockList, theCaseID

'''Add a new checkin entry to the chain of custody for the given evidence item. 
Checkin actions may only be performed on evidence items that have already been 
added to the blockchain.'''
def checkin(evidenceIDList):
    parse()
    maxTime = 0
    recentBlock = None

    #verify input
    if evidenceIDList == None:
        print("no evidence id provided!")
        exit(666)

    for evidenceID in evidenceIDList:
        for block in blockList:
            if evidenceID[0] == block.evidenceID:
                if block.timestamp > maxTime:
                    maxTime = max(maxTime, block.timestamp)
                    recentBlock = block

        #if the evidenceID doesn't exist
        if recentBlock == None:
            print("no block exists with that evidence id!")
            exit(666)

        tempState = "".join(e for e in recentBlock.state if e.isalnum())
        if tempState == "CHECKEDOUT":
            pHash = bytes(0x00)
            newBlock = Block(prevHash=pHash, 
            	caseID=recentBlock.caseID, 
            	evidenceID=evidenceID[0], 
            	state="CHECKEDIN", 
            	dataLength=0, 
            	data="" )
            data = newBlock.packData()
            blockFile = open(BCHOC_FILE_PATH, 'ab')
            blockFile.write(data)
            blockFile.close()
            blockList.append(newBlock)

            dt = datetime.datetime.fromtimestamp(newBlock.timestamp)
            dt_iso = dt.isoformat()
            print("Case: {c}".format(c=recentBlock.caseID))
            print("Checked out item: {i}".format(i=evidenceID[0]))
            print("\tStatus: CHECKEDIN")
            print("\tTime of action: {t}".format(t=dt_iso))

        else:
            print("block must be checkedin to be checked out!")
            exit(666)
    return