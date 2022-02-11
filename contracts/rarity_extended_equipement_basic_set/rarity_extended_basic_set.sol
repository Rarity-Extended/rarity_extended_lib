// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "../rERC721Enumerable.sol";
import "../extended.sol";

contract rarity_extended_basic_set is Extended, rERC721Enumerable {

    uint8 constant ARMOR_TYPE = 2;
    uint8 constant WEAPON_TYPE = 3;

    uint public next_item;
    uint public basicSetPrice;
    uint public setsIndex = 1;
    mapping(uint => BasicSet) public sets;
    mapping(uint => item) public items;

    struct item {
        uint8 base_type;
        uint8 item_type;
        uint32 crafted;
        uint crafter;
    }

    struct BasicSet {
        string setName;
        uint8 head;
        uint8 body;
        uint8 hand;
        uint8 foot;
        uint8 weapon;
    }

    constructor(address _rm, uint _basicSetPrice) ERC721(_rm) {
        basicSetPrice = _basicSetPrice;
    }

    /*******************************************************************************
    **  @notice: used for admin to extract money earned from sets sales
	*******************************************************************************/
    function getMoney() public onlyExtended {
        payable(msg.sender).transfer(address(this).balance);
    }

    /*******************************************************************************
    **  @dev: creates 4 new items (head, body, hand, foot, weapon). Saves on a registry
    **  @notice: creates a new set
    **  @param setName: name of the set
    **  @param headItemType: item type for the head armor
    **  @param bodyItemType: item type for the body armor
    **  @param handItemType: item type for the hand armor
    **  @param footItemType: item type for the foot armor
    **  @param weaponItemType: item type for the weapon
	*******************************************************************************/
    function deployNewSet(
        string memory setName,
        uint8 headItemType,
        uint8 bodyItemType,
        uint8 handItemType,
        uint8 footItemType,
        uint8 weaponItemType
    ) public onlyExtended {
        //Save on registry
        sets[setsIndex] = BasicSet(
            setName,
            headItemType,
            bodyItemType,
            handItemType,
            footItemType,
            weaponItemType
        );
        setsIndex++;
    }

    /*******************************************************************************
    **  @dev: mint a new set in exchange for `basicSetPrice`
    **  @notice: buys a new set paying the price
    **  @param setIndex: index of the set to buy
    **  @param receiver: summoner which will receive the set
	*******************************************************************************/
    function buySet(uint setIndex, uint receiver) public payable {
        require(msg.value == basicSetPrice, "!basicSetPrice");
        require(setIndex != 0, "!setIndex");

        uint32 timestamp = uint32(block.timestamp);

        BasicSet memory setToBuy = sets[setIndex];
        require(setToBuy.head != 0 && setToBuy.body != 0 && setToBuy.hand != 0 && setToBuy.foot != 0, "!emptySet");

        items[next_item] = item(ARMOR_TYPE, setToBuy.head, timestamp, receiver);
        _safeMint(receiver, next_item);
        next_item++;

        items[next_item] = item(ARMOR_TYPE, setToBuy.body, timestamp, receiver);
        _safeMint(receiver, next_item);
        next_item++;

        items[next_item] = item(ARMOR_TYPE, setToBuy.hand, timestamp, receiver);
        _safeMint(receiver, next_item);
        next_item++;

        items[next_item] = item(ARMOR_TYPE, setToBuy.foot, timestamp, receiver);
        _safeMint(receiver, next_item);
        next_item++;

        items[next_item] = item(WEAPON_TYPE, setToBuy.weapon, timestamp, receiver);
        _safeMint(receiver, next_item);
        next_item++;
    }

    /*******************************************************************************
    **  @notice: get type
    **  @return: a string name with the type name
	*******************************************************************************/
    function get_type(uint _type_id) public pure returns (string memory _type) {
       if (_type_id == 2) {
            _type = "Armor";
        } else if (_type_id == 3) {
            _type = "Weapons";
        }
    }

    /*******************************************************************************
    **  @notice: get all sets
    **  @return: an array of BasicSet
	*******************************************************************************/
    function getSets() public view returns (BasicSet[] memory) {
        uint _setsIndex = setsIndex - 1;
        BasicSet[] memory _sets = new BasicSet[](_setsIndex - 1);
        for (uint256 i = 0; i < _setsIndex; i++) {
            _sets[i] = sets[i];
        }
        return _sets;
    }

}