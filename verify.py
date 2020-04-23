
#!/usr/bin/env python3
import hashlib
import os.path
import sys
import datetime
import struct
import binascii
from Block import Block
from parse import parse, itemIDS, blockList, theCaseID, BCHOC_FILE_PATH



def verify():
	checkedinSet = []
	checkedoutSet = []
	prevSet= []
	removedSet = []
	parentSet = []
	hashSet = []
	removedReasonsSet = set(["DISPOSED", "DESTROYED", "RELEASED"])
	state = ["DISPOSED", "DESTROYED", "RELEASED", "CHECKEDIN", "CHECKEDOUT", "INITIAL"]
	errID = 0
	blockTot = 0
	errBlock = ""
	dupParentErr = ""
	prevHash = None
	prevBlock = None
	print(len(blockList))
	for blk in blockList:
		blockTot += 1
		thisBlockHash = blk.getHash().digest()
		this_state = blk.state.strip('\x00')
		print(hashSet)
		print(parentSet) 
		# If current block has no parent and is not INITIAL, give error (may need to change this to b'0x0000000000....')
		if ((prevHash == None) and (this_state != "INITIAL")):
			print("1")
			errID = 1
			errBlock = thisBlockHash

		elif prevHash == None and this_state == "INITIAL":
			errID = 0
		# If current block has the same prevHash as another block
		elif (prevHash in parentSet):
			print("2")
			errID = 2
			errBlock = thisBlockHash
			dupParentErr = prevHash

		elif (blk.prevHash in prevSet):
			print("2")
			errID = 2
			errBlock = thisBlockHash
			dupParentErr = prevHash

		# Checking current block against all CHECKEDIN blocks
		elif (this_state == "CHECKEDIN"):
			print("3")
			# If CHECKEDOUT, check item in
			if (blk.evidenceID in checkedoutSet):
				checkedinSet.append(blk.evidenceID)
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
				checkedinSet.append(blk.evidenceID)

		# Checking current block against all CHECKEDOUT blocks
		elif (this_state == "CHECKEDOUT"):
			print("4")
			# If item checked in, check item out
			if (blk.evidenceID in checkedinSet):
				checkedoutSet.append(blk.evidenceID)
				checkedinSet.remove(blk.evidenceID)
			# If CHECKEDOUT already, give error
			elif (blk.evidenceID in checkedoutSet):
				errID = 5
				errBlock = thisBlockHash
			# If REMOVED already, give error
			elif (blk.evidenceID in removedSet):
				errID = 6
				errBlock = thisBlockHash

		elif (this_state == "REMOVED"):
			print("5")
			# If item checked in, check item out
			if (blk.data == ""):
				errID = 12

		# Checking current block against all REMOVED blocks
		elif (this_state in removedReasonsSet):
			print("5")
			# If CHECKEDIN, remove item
			if (blk.evidenceID in checkedinSet):
				removedSet.append(blk.evidenceID)
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
		elif (this_state not in state):
			print("6")
			print(bytes(blk.state, 'utf-8'))
			print("state not in stateset")
			exit(666)

		# If this item is identical to one already in chain, give error
		elif (thisBlockHash in hashSet):
			print("7")
			errID = 10
			errBlock = thisBlockHash

		# If this item's has a different hash than it should (according to next block's prevHash), give error
		elif prevHash is not None and prevBlock is not None:
			print("8")
			if (prevHash != prevBlock.getHash().digest()):
				errID = 11
				errBlock = prevHash

		if prevHash is not None:
			parentSet.append(prevHash)
			if blk.prevHash[0:5] != prevHash[0:5]:
				print("")
				print("actual previous hash: " + str(blk.prevHash[0:5]) )
				print("expected previous hash: " + str(prevHash[0:5]) )
				errID = 2
				errBlock = thisBlockHash
				dupParentErr = prevHash

		hashSet.append(thisBlockHash)
		prevBlock = blk
		prevHash = thisBlockHash


	###############################################################################

	if len(set(hashSet)) != len(hashSet) or len(set(parentSet)) != len(parentSet):
			exit(666)

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

		elif (errID == 11):
			print ("Remove without owner.")
	exit(666)