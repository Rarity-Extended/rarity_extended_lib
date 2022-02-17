## RarityExtended Equipement Basic Set

Basic sets is a group of pre-fabricated Equipments for use in Rarity. You can buy a set and mount it in your summoner. 
Basic sets contracts extends [rERC721Enumerable](contracts/rERC721Enumerable.sol).

## Usage

To get the price of a set in FTM:

```js
function basicSetPrice() external view returns (uint);
```

To buy a set:

```js
function buySet(uint _id, uint _receiver) external payable;
```

To get owned sets:

```js
function getOwnedItems(uint _adventurerID) external view returns (item[] memory);
```

To get FTM earned from set sales (onlyExtended function):

```js
function getMoney() external;
```

## Detailed information

Sets are composed of 6 parts:

- Head
- Body
- Hand
- Foot
- Primary Weapon
- Secondary Weapon/shield

These can be changed and transferred individualy.