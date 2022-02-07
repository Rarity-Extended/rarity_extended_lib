// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "../rarity.sol";
import "../interfaces/IrERC20.sol";
import "../interfaces/IRarityFarmingCore.sol";

contract rarity_extended_farming_base is Rarity {
	uint constant DAY = 1 days; //Duration between two harvest
	uint constant MAX_REWARD_PER_HARVEST = 3; //Base rewards is between 1 and MAX_REWARD_PER_HARVEST 
	uint immutable public typeOf; //Type of farm. 1 for wood, 2 for minerals etc.
	uint public requiredLevel; //Required level to access this farm
	address[] public requiredItems; //What you need to unlock this farm
	uint[] public requiredItemsCount; //How many of what you need you need to unlock this farm
	string public name; //Name of the farm
	IrERC20 immutable farmLoot; //What you will get by using this farm
	IRarityFarmingCore immutable farmingCore; //Farm Core contract

    bool immutable defaultUnlocked; //Is this contract unlocked by default for any adventurer
	mapping(uint => bool) public isUnlocked; //Is this contract unlocked for adventurer uint
	mapping(uint => uint) public nextHarvest; //Next harvest for adventurer

    event Harvested(uint _adventurer, uint _amount);
    event Unlocked(uint _adventurer);

    /*******************************************************************************
    **  @dev Register the farming contract.
    **	@param _farmingType: Can be one of theses, but some more may be added
    **	- 1 for wood
    **	- 2 for minerals
    **	@param _farmingCore: Core farming contract
    **	@param _farmLoot: Loot item farmed by this contract
    **	@param _name: Name of this contract
    **	@param _requiredLevel: Level required to access this farm
    **	@param _requiredItems: List of loot items required to unlock this farm
    **	@param _requiredItemsCount: Amount of loots required to unlock this farm
    *******************************************************************************/
	constructor(
        uint8 _farmingType,
        address _farmingCore,
        address _farmLoot,
        string memory _name,
        uint _requiredLevel,
        address[] memory _requiredItems,
        uint[] memory _requiredItemsCount
    ) Rarity(true) {
        require(_requiredItems.length == _requiredItemsCount.length);
		typeOf = _farmingType;
        farmingCore = IRarityFarmingCore(_farmingCore);
        farmLoot = IrERC20(_farmLoot);
        name = _name;
        requiredLevel = _requiredLevel;
		requiredItems = _requiredItems;
		requiredItemsCount = _requiredItemsCount;
        defaultUnlocked = _requiredItems.length == 0;
	}

    /*******************************************************************************
    **  @dev Allow an adventurer to unlock the farm if the requirement are met.
    **	@param _adventurer: adventurer we would like to use with this farm
    *******************************************************************************/
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
        emit Unlocked(_adventurer);
	}

    /*******************************************************************************
    **  @dev Perform an harvest with an adventurer. You have to be the owner of the
    **  adventurer, nextHarvest should be before now, the requirements must be met.
    **  On success, set the next harvest to now + 1 day and increase XP for this
    **  farming type
    **	@param _adventurer: adventurer we would like to use with this farm
    *******************************************************************************/
    function harvest(uint _adventurer) public {
        require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
        require(block.timestamp > nextHarvest[_adventurer], "!nextHarvest");
        require(farmingCore.level(_adventurer, typeOf) >= requiredLevel, "!level");
		require(isUnlocked[_adventurer] || defaultUnlocked, "!unlocked");
        nextHarvest[_adventurer] = block.timestamp + DAY;
        farmingCore.earnXp(_adventurer);
        uint harvestAmount = _mintFarmLoot(_adventurer);
        emit Harvested(_adventurer, harvestAmount);
    }

    /*******************************************************************************
    **  @dev mint the rewards for the adventurer. The rewards are set in two random
    **  parts, one based on a basic random from 1 to MAX_REWARD_PER_HARVEST, and one
    **  based on adventurer level, from 0 to the level
    **	@param _adventurer: adventurer we would like to use with this farm
    *******************************************************************************/
	function _mintFarmLoot(uint _adventurer) internal returns (uint) {
		uint adventurerLevel = farmingCore.level(_adventurer, typeOf);
		uint farmLootAmount = _get_random(_adventurer, MAX_REWARD_PER_HARVEST, false);
        uint extraFarmLootAmount = _get_random(_adventurer, adventurerLevel, true);
		farmLoot.mint(_adventurer, extraFarmLootAmount + farmLootAmount);
		return extraFarmLootAmount + farmLootAmount;
	}

    /*******************************************************************************
    **  @dev Random number generator
    **	@param _adventurer: some seed
    **	@param _limit: max amount expected
    **	@param _withZero: [0 - X] or [1 - X]
    *******************************************************************************/
    function _get_random(uint _adventurer, uint _limit, bool _withZero) internal view returns (uint) {
        _adventurer += gasleft();
        uint result = 0;
        if (_withZero) {
            if (_limit == 0) {
                return 0;
            }
            result = _random.dn(_adventurer, _limit);
        } else {
            if (_limit == 1) {
                return 1;
            }
            result = _random.dn(_adventurer, _limit);
            result += 1;
        }
        return result;
    }
}