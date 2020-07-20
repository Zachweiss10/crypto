# Crypto Project

This creates and maintains a blockchain for a forensics department enabling proper tracking of items that are checked into evidence.

You can a initialize a block chain, check in new evidence, check out new evidence, parse the blockchain, remove, and verify the integrity of the blockchain.

some constraints: 
1. Only a single person can check out an item at a time (to ensure proper chain of custody)
2. Each added node needs to have a hashed version of the previous (parent) node of the chain and a time stamp (this is how verification is established)
3. Removed evidence items will not be removed from the block chain but instead be marked as "REALEASED" and properly logged. This ensured the verification and chain of custody remain intact.


