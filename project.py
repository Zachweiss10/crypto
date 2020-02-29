#!/usr/bin/env python3

import hashlib
import os.path
import sys
import datetime
import struct

BCHOC_FILE_PATH = "./blocParty"

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
        currTime = datetime.datetime.now(datetime.timezone.utc)
        packedData = struct.pack("20s d 16s I 11s I 14s", bytes(0x00), float(currTime.strftime("%s.%f")), bytes(0x00), 0, str.encode("INITIAL"), 14, str.encode("Initial block"))
        blockFile = open(BCHOC_FILE_PATH, 'wb')
        blockFile.write(packedData)
        blockFile.close()
        print("Blockchain file not found. Created INITIAL block.")
        dieWithSuccess()

else:
    dieWithError()
