// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "../extended.sol";
import "../rarity.sol";
import "../interfaces/IRarity.sol";
import "../interfaces/IRarityFarmBase.sol";

contract rarity_extended_farming_wrapper is Extended {
	string constant public name  = "Rarity Extended Farming Wrapper";
	uint constant XP_PER_HARVEST = 250;

	constructor() Extended() {}

	struct sFarm {
		uint typeOf;
		uint tier;
	}

	//Farm contract -> farmingType
	mapping(address => sFarm) public Farm;

	//adventurer -> farmingType -> leve
	mapping(uint => mapping(uint => uint)) public level;

	//adventurer -> farmingType -> xp
	mapping(uint => mapping(uint => uint)) public xp;

	//adventurer -> farm -> nextHarvest
	mapping(uint => mapping(address => uint)) public nextHarvest;

	/*******************************************************************************
	**  @dev Assign a new farm contract to a farm index. As time of deployment
	**  slots are: 
	**  - 0 -> undefined
	**  - 1 -> Wood
	**  - 2 -> Mining
	**  - 3 -> Herbalist
	**  - 4 -> Fishing
	**	@param _farm: Address of the farm contract
	*******************************************************************************/
	function registerFarm(address _farm) public onlyExtended() {
		require(_farm != address(0), "!address");
		uint8 farmType = IRarityFarmBase(_farm).typeOf();
		uint8 farmRequiredLevel = IRarityFarmBase(_farm).requiredLevel();
		require(farmType != 0, "!farm");
		require(Farm[_farm].typeOf == 0, '!new');
		Farm[_farm] = sFarm(farmType, farmRequiredLevel);
	}

	function setNextHarvest(uint _adventurer, uint _delay) external returns (uint) {
		sFarm memory farm = Farm[msg.sender];
		require(farm.typeOf != 0, "!farm");
		nextHarvest[_adventurer][msg.sender] = block.timestamp + _delay;
		return nextHarvest[_adventurer][msg.sender];
	}

	function setXp(uint _adventurer) external returns (uint) {
		sFarm memory farm = Farm[msg.sender];
		require(farm.typeOf != 0, "!farm");
		uint256 xpProgress = XP_PER_HARVEST - (XP_PER_HARVEST * (level[_adventurer][farm.typeOf] - farm.tier) * 20 / 100);
		xp[_adventurer][farm.typeOf] += xpProgress;
		return xp[_adventurer][farm.typeOf];
	}

	function getNextHarvest(uint _adventurer) external view returns (uint) {
		return nextHarvest[_adventurer][msg.sender];
	}

    function xpRequired(uint curent_level) public pure returns (uint) {
        return (curent_level * (curent_level + 1) / 2) * 1000;
    }
}

