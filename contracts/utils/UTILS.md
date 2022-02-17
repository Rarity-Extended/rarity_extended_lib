## Utils
OpenZeppelin libraries (used in rERC721 implementation) and rERC721 standard.

#### ECDSA
[See OZ docs](https://docs.openzeppelin.com/contracts/4.x/api/utils#ECDSA)

#### rERC721
ERC721 implementation for Rarity Manifested. See original standard [in OZ docs](https://docs.openzeppelin.com/contracts/4.x/api/token/erc721).

#### Strings
[See OZ docs](https://docs.openzeppelin.com/contracts/4.x/api/utils#Strings)

#### RarityExtended ERC20
Variant of the ERC20 standard used for the Rarity specific adventurer system.
Used by Rarity Extended.

*Original work by TheAustrian for the Boars Adventure.*

#### RarityExtended ERC721 Enumerable
Variant of the ERC721 standard used for the Rarity specific adventurer system.
Used by Rarity Extended.

Modified to use UINT in ADDRESS. 
In this case, we attach this NFT to another NFT.
Note that uint(0) is equivalent to address(0), so holder of the first NFT is burner address and can't access to some functions in contract.

## RarityExtended Loot
Loot items used in [boars adventure](https://github.com/Rarity-Extended/rarity_extended_boars), and other contracts. Extends rERC20.