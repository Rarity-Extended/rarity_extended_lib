## RarityExtended Equipement Basic Set

Basic sets is a group of pre-fabricated Equipments for use in Rarity. You can buy a set and mount it in your summoner. 
Basic sets contracts extends [rERC721Enumerable](contracts/utils/rERC721Enumerable.sol).
Metadata of parts can be found in Codexes: [here for armor](rarity_extended_basic_set_armor_codex.sol) and [here for weapons](rarity_extended_basic_set_weapon_codex.sol).

Sets are composed of 6 parts:

- Head
- Body
- Hand
- Foot
- Primary Weapon
- Secondary Weapon/shield

These can be changed and transferred individualy.

## Usage

#### SET functions

To buy a set:

```js
function buySet(uint _id, uint _receiver) external payable;
```

To receive FTM earned from set sales (onlyExtended function):

```js
function getMoney() external;
```

#### GET functions

To get owned sets:

```js
function getOwnedItems(uint _adventurerID) external view returns (item[] memory);
```

To get the price of a set in FTM:

```js
function basicSetPrice() external view returns (uint);
```

**[Deployed here](../../../DEPLOYEDCONTRACTS.md#BasicSet)**