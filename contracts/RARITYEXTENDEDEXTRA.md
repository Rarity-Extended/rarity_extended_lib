## RarityExtended ERC20
Variant of the ERC20 standard used for the Rarity specific adventurer system.
Used by Rarity Extended.

*Original work by TheAustrian for the Boars Adventure.*

------

## RarityExtended ERC721 Enumerable
Variant of the ERC721 standard used for the Rarity specific adventurer system.
Used by Rarity Extended.

Modified to use UINT in ADDRESS. 
In this case, we attach this NFT to another NFT.
Note that uint(0) is equivalent to address(0), so holder of the first NFT is burner address and can't access to some functions in contract.

------

## RarityExtended Extended
Variant of the onlyOwner contract. Used to restrict access of some functions.

------