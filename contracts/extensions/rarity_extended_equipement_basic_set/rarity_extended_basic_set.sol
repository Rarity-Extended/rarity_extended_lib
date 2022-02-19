// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "../../utils/rERC721Enumerable.sol";
import "../../extended.sol";

contract rarity_extended_basic_set is rERC721Enumerable {
    address immutable REWARD_ADDRESS;
    string constant public name = "Rarity Extended Basic Sets";
    uint8 constant ARMOR_TYPE = 2;
    uint8 constant WEAPON_TYPE = 3;
    uint256 immutable public basicSetPrice;
    uint public next_item = 1;
    mapping(uint => item) public items;

    struct item {
        uint8 base_type;
        uint8 item_type;
        uint32 crafted;
        uint crafter;
        uint tokenID;
    }

    constructor(address _rm, address _rewardAddress, uint _basicSetPrice) rERC721(_rm, "Basic Set") {
        REWARD_ADDRESS = _rewardAddress;
        basicSetPrice = _basicSetPrice;
    }

    /*******************************************************************************
    **  @dev: mint a new set in exchange for `basicSetPrice`
    **  @notice: buys a new set paying the price
    **  @param setIndex: index of the set to buy
    **  @param receiver: summoner which will receive the set
	*******************************************************************************/
    function buySet(uint _id, uint _receiver) public payable {
        require(msg.value == basicSetPrice, "!basicSetPrice");
        require(_id > 0 && _id < 12, "!id");
        payable(REWARD_ADDRESS).transfer(basicSetPrice);

        uint32 timestamp = uint32(block.timestamp);
        uint8[6] memory set = set_by_id(_id);
        for (uint256 index = 0; index < 6; index++) {
            if (set[index] == 0) {
                continue;
            }
            uint8 base_type = (index == 4 || (index == 5 && set[index] != 19)) ? WEAPON_TYPE : ARMOR_TYPE;
            items[next_item] = item(base_type, set[index], timestamp, _receiver, next_item);
            _safeMint(_receiver, next_item++);
            
        }
    }

    /*******************************************************************************
    **  @notice: Return the name of a set by it's ID
	*******************************************************************************/
    function get_set_by_id(uint _id) public pure returns (string memory description) {
        if (_id == 1) return ('Barbarian Basic Set');
        if (_id == 2) return ('Bard Basic Set');
        if (_id == 3) return ('Cleric Basic Set');
        if (_id == 4) return ('Druid Basic Set');
        if (_id == 5) return ('Fighter Basic Set');
        if (_id == 6) return ('Monk Basic Set');
        if (_id == 7) return ('Paladin Basic Set');
        if (_id == 8) return ('Ranger Basic Set');
        if (_id == 9) return ('Rogue Basic Set');
        if (_id == 10) return ('Sorcerer Basic Set');
        if (_id == 11) return ('Wizard Basic Set');
        return ('');
    }

    /*******************************************************************************
    **  @notice: Return the items from the set included. Order is:
    **  -> Head | Body | Hand | Foot | Primary Weapon | Secondary Weapon/shield
	*******************************************************************************/
    function set_by_id(uint _id) public pure returns(uint8[6] memory) {
        if (_id == 1) return ([15, 4, 9, 13, 4, 0]);
        if (_id == 2) return ([17, 1, 7, 12, 1, 0]);
        if (_id == 3) return ([15, 5, 10, 13, 3, 19]);
        if (_id == 4) return ([15, 4, 9, 13, 2, 19]);
        if (_id == 5) return ([18, 6, 11, 14, 5, 19]);
        if (_id == 6) return ([15, 1, 8, 12, 8, 0]);
        if (_id == 7) return ([18, 6, 11, 14, 6, 19]);
        if (_id == 8) return ([15, 3, 7, 12, 7, 0]);
        if (_id == 9) return ([15, 3, 7, 12, 1, 1]);
        if (_id == 10) return ([16, 2, 7, 12, 9, 0]);
        if (_id == 11) return ([16, 2, 7, 12, 9, 0]);
        return ([0, 0, 0, 0, 0, 0]);
    }

    /*******************************************************************************
    **  @notice: Retrieve all the items for an adventurer
	*******************************************************************************/
    function getOwnedItems(uint _adventurerID) public view returns (item[] memory) {
        require(_adventurerID != uint(0), "cannot retrieve zero address");
        uint256 arrayLength = balanceOf(_adventurerID);
        item[] memory _ownedItems = new item[](arrayLength);
        for (uint256 i = 0; i < arrayLength; i++) {
            uint256 tokenId = tokenOfOwnerByIndex(_adventurerID, i);
            _ownedItems[i] = items[tokenId];
        }
        return _ownedItems;
    }
}