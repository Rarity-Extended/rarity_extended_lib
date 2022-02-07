// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "../rarity.sol";
import "../interfaces/IrERC20.sol";
import "../interfaces/IRarityFarmingWrapper.sol";

contract rarity_extended_farming_base is Rarity {
    uint constant DEFAULT_XP_REQUIRED = 1_000;
	uint constant DAY = 1 days;
	uint8 constant public MAX_REWARD_PER_HARVEST = 3;
	uint8 immutable public typeOf;
	string public name;

	uint public requiredLevel;
	address[] public requiredItems;
	uint[] public requiredItemsCount;

	IrERC20 immutable farmLoot;
	IRarityFarmingWrapper immutable wrapper;

    bool defaultUnlocked;
	mapping(uint => bool) public isUnlocked;

	/*******************************************************************************
    **  @dev Register the abstract contract.
    **	@param _farmingType: Can be one of theses, but some more may be added
	**	- 1 for wood
	**	- 2 for minerals
	**	- 3 for plants
	**	- 4 for fishing
	*******************************************************************************/
	constructor(
        uint8 _farmingType,
        address _wrapper,
        address _farmLoot,
        string memory _name,
        uint _requiredLevel,
        address[] memory _requiredItems,
        uint[] memory _requiredItemsCount
    ) Rarity(true) {
        require(_requiredItems.length == _requiredItemsCount.length);
		typeOf = _farmingType;
        wrapper = IRarityFarmingWrapper(_wrapper);
        farmLoot = IrERC20(_farmLoot);
        name = _name;
        requiredLevel = _requiredLevel;
		requiredItems = _requiredItems;
		requiredItemsCount = _requiredItemsCount;
        defaultUnlocked = _requiredItems.length == 0;
	}

	function unlock(uint _adventurer) public {
        require(!defaultUnlocked, "!unlocked");
        require(!isUnlocked[_adventurer], "!unlocked");
		require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
		for (uint256 i = 0; i < requiredItems.length; i++) {
			IrERC20(requiredItems[i]).transferFrom(
				RARITY_EXTENDED_NCP,
				_adventurer,
				RARITY_EXTENDED_NCP,
				requiredItemsCount[i]
			);
		}
		isUnlocked[_adventurer] = true;
	}

    function harvest(uint _adventurer) external {
        require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
        require(block.timestamp > wrapper.getNextHarvest(_adventurer), "!nextHarvest");
        require(wrapper.level(_adventurer, typeOf) >= requiredLevel, "!level");
		require(isUnlocked[_adventurer] || defaultUnlocked, "!unlocked");
        wrapper.setNextHarvest(_adventurer, DAY);
        wrapper.setXp(_adventurer);
        _mintFarmLoot(_adventurer);
    }

	function _mintFarmLoot(uint _adventurer) internal returns (uint) {
		uint adventurerLevel = wrapper.level(_adventurer, typeOf);
		uint farmLootAmount = _get_random(_adventurer, MAX_REWARD_PER_HARVEST, false);
        uint extraFarmLootAmount = _get_random(_adventurer, adventurerLevel, true);
		farmLoot.mint(_adventurer, extraFarmLootAmount + farmLootAmount);
		return extraFarmLootAmount + farmLootAmount;
	}

    function _get_random(uint _adventurer, uint limit, bool withZero) internal view returns (uint) {
        _adventurer += gasleft();
        uint result = 0;
        if (withZero) {
            if (limit == 0) {
                return 0;
            }
            result = _random.dn(_adventurer, limit);
        } else {
            if (limit == 1) {
                return 1;
            }
            result = _random.dn(_adventurer, limit);
            result += 1;
        }
        return result;
    }
}