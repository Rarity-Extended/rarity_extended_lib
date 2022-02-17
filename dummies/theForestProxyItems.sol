// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface ITheRarityForestV3 {
    function transferFrom(uint from, uint to, uint256 tokenId) external;
    function treasure(uint tokenId) external view returns (uint _summonerId, string memory _itemName, uint _magic, uint _level);
    function ownerOf(uint256 tokenId) external view returns (uint owner);
    function saveTreasure(uint256 tokenId) external;
}

contract theForestProxyItems {
	ITheRarityForestV3 public _forest = ITheRarityForestV3(0x48e6F88F1Ab05677675dE9d14a705f8A137ea2bC);

    struct item {
        uint8 base_type; // 1 for goods, 2 for armor, 3 for weapon, 4 for jewelries
        uint8 item_type; // ID of the item type (not the tokenID)
		uint32 _standard_field_one;
        uint _standard_field_two;
    }

    function get_type(uint _type_id) public pure returns (string memory _type) {
        if (_type_id == 1) {
            _type = "Goods";
        } else if (_type_id == 2) {
            _type = "Armor";
        } else if (_type_id == 3) {
            _type = "Weapons";
        } else if (_type_id == 4) {
            _type = "Jewelries";
        }
    }

    function isValid(uint _base_type, uint _item_type) public pure returns (bool) {
        if (_base_type == 1) {
            return (1 <= _item_type && _item_type <= 34);
        } else if (_base_type == 2) {
            return (1 <= _item_type && _item_type <= 4);
        } else if (_base_type == 3) {
            return (1 <= _item_type && _item_type <= 7);
        } else if (_base_type == 4) {
            return (1 <= _item_type && _item_type <= 11);
        }
        return false;
    }

    function items(uint _itemID) public view returns (item memory) {
        (,string memory _itemName,,) = _forest.treasure(_itemID);

		//Goods
		if (compareStrings(_itemName, "Dead King crown")) return (item(1, 1, 0, 0));
		if (compareStrings(_itemName, "Ancient book")) return (item(1, 2, 0, 0));
		if (compareStrings(_itemName, "Enchanted book")) return (item(1, 3, 0, 0));
		if (compareStrings(_itemName, "Treasure map")) return (item(1, 4, 0, 0));
		if (compareStrings(_itemName, "Spell book")) return (item(1, 5, 0, 0));
		if (compareStrings(_itemName, "Old damaged coin")) return (item(1, 6, 0, 0));
		if (compareStrings(_itemName, "Dragon egg")) return (item(1, 7, 0, 0));
		if (compareStrings(_itemName, "War helmet")) return (item(1, 8, 0, 0));
		if (compareStrings(_itemName, "Fire boots")) return (item(1, 9, 0, 0));
		if (compareStrings(_itemName, "Enchanted useless tool")) return (item(1, 10, 0, 0));
		if (compareStrings(_itemName, "War trophy")) return (item(1, 11, 0, 0));
		if (compareStrings(_itemName, "Elf skull")) return (item(1, 12, 0, 0));
		if (compareStrings(_itemName, "War book")) return (item(1, 13, 0, 0));
		if (compareStrings(_itemName, "Gold pot")) return (item(1, 14, 0, 0));
		if (compareStrings(_itemName, "Demon head")) return (item(1, 15, 0, 0));
		if (compareStrings(_itemName, "Unknown key")) return (item(1, 16, 0, 0));
		if (compareStrings(_itemName, "Cursed book")) return (item(1, 17, 0, 0));
		if (compareStrings(_itemName, "Giant plant seed")) return (item(1, 18, 0, 0));
		if (compareStrings(_itemName, "Bear claw")) return (item(1, 19, 0, 0));
		if (compareStrings(_itemName, "Glove with diamonds")) return (item(1, 20, 0, 0));
		if (compareStrings(_itemName, "Warrior watch")) return (item(1, 21, 0, 0));
		if (compareStrings(_itemName, "Paladin eye")) return (item(1, 22, 0, 0));
		if (compareStrings(_itemName, "Metal horse saddle")) return (item(1, 23, 0, 0));
		if (compareStrings(_itemName, "Witcher book")) return (item(1, 24, 0, 0));
		if (compareStrings(_itemName, "Witch book")) return (item(1, 25, 0, 0));
		if (compareStrings(_itemName, "Unknown animal eye")) return (item(1, 26, 0, 0));
		if (compareStrings(_itemName, "Shadowy rabbit paw")) return (item(1, 27, 0, 0));
		if (compareStrings(_itemName, "Red Tanned Gloves")) return (item(1, 28, 0, 0));
		if (compareStrings(_itemName, "Paladin heart")) return (item(1, 29, 0, 0));
		if (compareStrings(_itemName, "Cat Claw glove")) return (item(1, 30, 0, 0));
		if (compareStrings(_itemName, "Skull fragment")) return (item(1, 31, 0, 0));
		if (compareStrings(_itemName, "Hawk eye")) return (item(1, 32, 0, 0));
		if (compareStrings(_itemName, "Meteorite fragment")) return (item(1, 33, 0, 0));
		if (compareStrings(_itemName, "Mutant fisheye")) return (item(1, 34, 0, 0));

		//Armors
		if (compareStrings(_itemName, "Haunted cloak")) return (item(2, 1, 0, 0));
		if (compareStrings(_itemName, "Dead hero cape")) return (item(2, 2, 0, 0));
		if (compareStrings(_itemName, "Slain warrior armor")) return (item(2, 3, 0, 0));
		if (compareStrings(_itemName, "It's a random shield")) return (item(2, 4, 0, 0));

		//Weapons
        if (compareStrings(_itemName, "Black gauntlet")) return (item(3, 1, 0, 0));
        if (compareStrings(_itemName, "Silver sword")) return (item(3, 2, 0, 0));
        if (compareStrings(_itemName, "Ancient Prince Andre's Sword")) return (item(3, 3, 0, 0));
        if (compareStrings(_itemName, "Mechanical hand")) return (item(3, 4, 0, 0));
        if (compareStrings(_itemName, "King's son sword")) return (item(3, 5, 0, 0));
        if (compareStrings(_itemName, "Thunder hammer")) return (item(3, 6, 0, 0));
        if (compareStrings(_itemName, "Old farmer sickle")) return (item(3, 7, 0, 0));

		//Jewelry
		if (compareStrings(_itemName, "Haunted ring")) return (item(4,1, 0, 0));
		if (compareStrings(_itemName, "Gold ring")) return (item(4,2, 0, 0));
		if (compareStrings(_itemName, "Magic necklace")) return (item(4,3, 0, 0));
		if (compareStrings(_itemName, "Unknown ring")) return (item(4,4, 0, 0));
		if (compareStrings(_itemName, "Silver ring")) return (item(4,5, 0, 0));
		if (compareStrings(_itemName, "Cursed talisman")) return (item(4,6, 0, 0));
		if (compareStrings(_itemName, "Rare ring")) return (item(4,7, 0, 0));
		if (compareStrings(_itemName, "Enchanted talisman")) return (item(4,8, 0, 0));
		if (compareStrings(_itemName, "Time crystal")) return (item(4,9, 0, 0));
		if (compareStrings(_itemName, "Antique ring")) return (item(4,10, 0, 0));
		if (compareStrings(_itemName, "Wolf necklace")) return (item(4,11, 0, 0));
		
        return item(0, 0, 0, 0);
    }
	
    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
}
