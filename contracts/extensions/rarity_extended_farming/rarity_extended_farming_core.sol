// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "../../extended.sol";
import "../../rarity.sol";
import "../../interfaces/IRarity.sol";
import "../../interfaces/IRarityFarmBase.sol";

contract rarity_extended_farming_core is Extended, Rarity {
	string constant public NAME  = "Rarity Extended Farming Core";
	uint constant public XP_PER_HARVEST = 250;

	constructor() Rarity(false) {}

	/*******************************************************************************
	**  @dev Structure to hold the farm. There is two informations:
	**  - typeOf, aka type of farm (1 for wood, 2 minerals, etc.)
	**	- tier, aka level of the farm, rarity tier.
	*******************************************************************************/
	struct Farm {
		uint typeOf;
		uint tier;
	}

	mapping(address => Farm) public farm; //farm contract -> farmingType
	mapping(uint => mapping(uint => uint)) public level; //adventurer -> farmingType -> level
	mapping(uint => mapping(uint => uint)) public xp; //adventurer -> farmingType -> xp

	/*******************************************************************************
	**  @dev Assign a new farm contract to a farm index. As time of deployment
	**  slots are: 0 -> undefined, 1 -> Wood, 2 -> Mining.
	**	Any number of farm can be added, but a whitelisting is used to try to avoid
	**	breaking the unbalanced balance. (we are trying to balance if, not easy).
	**	@param _farm: Address of the farm contract
	*******************************************************************************/
	function registerFarm(address _farm) public onlyExtended() {
		require(_farm != address(0), "!address");
		uint8 farmType = IRarityFarmBase(_farm).typeOf();
		uint8 farmRequiredLevel = IRarityFarmBase(_farm).requiredLevel();
		require(farmType != 0, "!farm");
		require(farm[_farm].typeOf == 0, '!new');
		farm[_farm] = Farm(farmType, farmRequiredLevel);
	}

	/*******************************************************************************
	**  @dev Revoke an existing farm 
	**	@param _farm: Address of the farm contract
	*******************************************************************************/
	function revokeFarm(address _farm) public onlyExtended() {
		require(farm[_farm].typeOf != 0, '!exist');
		farm[_farm] = Farm(0, 0);
	}

	/*******************************************************************************
	**  @dev Give some XP to the _adventurer. Only a registered farm can do that.
	**	The amount of XP earned is computed based on the level of the adventurer and
	**	the level of the harvest he is using.
	**	The XP is shared for all the farm with the same typeOf.
	**	@param _adventurer: adventurer to give some XP
	*******************************************************************************/
	function earnXp(uint _adventurer) public returns (uint) {
		Farm memory _farm = farm[msg.sender];
		require(_farm.typeOf != 0, "!farm");
		uint256 xpProgress = XP_PER_HARVEST - (XP_PER_HARVEST * (level[_adventurer][_farm.typeOf] - _farm.tier) * 20e8 / 100e8);
		xp[_adventurer][_farm.typeOf] += xpProgress;
		return xp[_adventurer][_farm.typeOf];
	}

	/*******************************************************************************
	**  @dev Trigger a level-up for an adventurer if enough XP is available. This
	**	will increase the loot and unlock new farms.
	**	@param _adventurer: adventurer to level-up
	**	@param _farmType: type of farm to level-up the adventurer for
	*******************************************************************************/
	function levelup(uint _adventurer, uint _farmType) external returns (uint) {
		require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
		uint currentLevel = level[_adventurer][_farmType];
		uint currentXP = xp[_adventurer][_farmType];
		uint requiredXP = xpRequired(currentLevel + 1);
		require(currentXP >= requiredXP, "!xp");
		
		level[_adventurer][_farmType] += 1;
		xp[_adventurer][_farmType] -= requiredXP;
		return level[_adventurer][_farmType];
	}

	/*******************************************************************************
	**  @dev Compute the XP required for the next level for a given level
	**	@param _currentLevel: current level to work with
	*******************************************************************************/
	function xpRequired(uint _currentLevel) public pure returns (uint) {
		return (_currentLevel * (_currentLevel + 1) / 2) * 1000;
	}

	/*******************************************************************************
	**  @dev For a specific adventurer and farm, return it's current status.
	**	@param _currentLevel: current level to work with
	**	@param _farmType: type of farm to work with
	*******************************************************************************/
	function adventurerStatus(uint _adventurer, uint _farmType) public view returns (uint, uint) {
		return (level[_adventurer][_farmType], xp[_adventurer][_farmType]);
	}
}

