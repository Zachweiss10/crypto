#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
from Block import Block, BCHOC_FILE_PATH
from parse import parse, itemIDS, blockList, theCaseID

checkedinSet = set()
checkedoutSet = set()
removedSet = set()
parentSet = set()
hashSet = set()
removedReasonsSet = set("DISPOSED", "DESTROYED", "RELEASED")
errID = 0
blockTot = 0
errBlock = ""
dupParentErr = ""

parse()

for blk in blockList:

    blockTot += 1
    thisBlockHash = blk.getHash()

    # If current block has no parent and is not INITIAL, give error (may need to change this to b'0x0000000000....')
    if ((blk.prevHash == None) and (blk.state != "INITIAL")):
        errID = 1
        errBlock = thisBlockHash

    # If current block has the same prevHash as another block
    elif (blk.prevHash in parentSet):
        errID = 2
        errBlock = thisBlockHash
        dupParentErr = blk.prevHash

    # Checking current block against all CHECKEDIN blocks
    elif (blk.state == "CHECKEDIN"):
        # If CHECKEDOUT, check item in
        if (blk.evidenceID in checkedoutSet):
            checkedinSet.add(blk.evidenceID)
            checkedoutSet.remove(blk.evidenceID)
        # If CHECKEDIN already, give error
        elif (blk.evidenceID in checkedinSet):
            errID = 3
            errBlock = thisBlockHash
        # If REMOVED already, give error
        elif (blk.evidenceID in removedSet):
            errID = 4
            errBlock = thisBlockHash
        # If new item, add to checked in list
        else:
            checkedinSet.add(blk.evidenceID)

    # Checking current block against all CHECKEDOUT blocks
    elif (blk.state = "CHECKEDOUT"):
        # If item checked in, check item out
        if (blk.evidenceID in checkedinSet):
            checkedoutSet.add(blk.evidenceID)
            checkedinSet.remove(blk.evidenceID)
        # If CHECKEDOUT already, give error
        elif (blk.evidenceID in checkedoutSet):
            errID = 5
            errBlock = thisBlockHash
        # If REMOVED already, give error
        elif (blk.evidenceID in removedSet):
            errID = 6
            errBlock = thisBlockHash

    # Checking current block against all REMOVED blocks
    elif (blk.state in removedReasonsSet):
        # If CHECKEDIN, remove item
        if (blk.evidenceID in checkedinSet):
            removedSet.add(blk.evidenceID)
            checkedinSet.remove(blk.evidenceID)
        # If CHECKEDOUT already, give error
        elif (blk.evidenceID in checkedoutSet):
            errID = 7
            errBlock = thisBlockHash
        # If REMOVED already, give error
        elif (blk.evidenceID in removedSet):
            errID = 8
            errBlock = thisBlockHash
        # If removed before add, give error
        else:
            errID = 9
            errBlock = thisBlockHash

    # If this item is identical to one already in chain, give error
    elif (thisBlockHash in hashSet):
        errID = 10
        errBlock = thisBlockHash

    # If this item's has a different hash than it should (according to next block's prevHash), give error
    elif (blk.prevHash != prevBlock.getHash()):
        errID = 11
        errBlock = blk.prevHash

    else:
        parentSet.add(blk.prevHash)
        hashSet.add(thisBlockHash)
        prevBlock = blk

###############################################################################

print ("Transactions in blockchain: {0}".format(blockTot))

if (errID == 0):
    print ("State of blockchain: CLEAN")
    exit(0)

elif (errID != 0):
    print ("State of blockchain: ERROR")
    print ("Bad block: {0}".format(errBlock))

    if (errID == 1):
        print ("Parent block not found.")

    elif (errID == 2):
        print ("Parent block: {0}".format(dupParentErr))
        print ("Two blocks found with same parent.")

    elif (errID == 3):
        print ("Double checkin error.")

    elif (errID == 4):
        print ("Checkin after removed error.")

    elif (errID == 5):
        print ("Double checkout error.")

    elif (errID == 6):
        print ("Checkout after remove error.")

    elif (errID == 7):
        print ("Remove after checkout error.")

    elif (errID == 8):
        print ("Double remove error.")

    elif (errID == 9):
        print ("Remove before add error.")

    elif (errID == 10):
        print ("Item already in chain error.")

    elif (errID == 11):
        print ("Block contents do not match block checksum.")

    exit(666)
