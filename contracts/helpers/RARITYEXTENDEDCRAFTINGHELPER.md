## RarityExtended Crafting Helper

Crafting Helper is a tool to facilitate the process of crafting on the original rarity crafting contract.

## Usage

#### SET functions

To try to craft an item:

```js
function craft(uint _adventurer, uint8 _base_type, uint8 _item_type, uint _crafting_materials) external;
```

#### GET functions

To get items by address:

```js
function getItemsByAddress(address _owner) public view returns (Item[] memory);
```

**[Deployed here]()**