#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import uuid
import struct
BCHOC_FILE_PATH = os.environ['BCHOC_FILE_PATH'].strip()

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
        uuidItem = uuid.UUID(self.caseID)
        fmtString = "20s d 16s I 11s I {dataLength}s".format(dataLength=self.dataLength)
        packedData = struct.pack(fmtString, self.prevHash, self.timestamp, uuidItem.bytes, self.evidenceID,
                                 self.state.encode(), self.dataLength, self.data.encode())
        self._dataString = packedData
        self._hash = hashlib.sha1(packedData)
        return packedData

    def unpackData(self, data):
        unpackedData = struct.unpack_from("20s d 16s I 11s I", data, 0)
        self.prevHash = unpackedData[0]
        self.timestamp = unpackedData[1]
        self.caseID = str(uuid.UUID(bytes=unpackedData[2]))
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
