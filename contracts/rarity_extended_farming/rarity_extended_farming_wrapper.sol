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

	//Farm contract -> farmingType
	mapping(address => uint) public farms;

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
		uint8 farmType = IRarityFarmBase(_farm).farm();
		require(farmType != 0, "!farm");
		require(farms[_farm] == 0, '!new');
		farms[_farm] = farmType;
	}

	function setNextHarvest(uint _adventurer, uint _delay) external returns (uint) {
		uint farm = farms[msg.sender];
		require(farm != 0, "!farm");
		nextHarvest[_adventurer][msg.sender] = block.timestamp + _delay;
		return nextHarvest[_adventurer][msg.sender];
	}

	function setXp(uint _adventurer) external returns (uint) {
		uint farm = farms[msg.sender];
		require(farm != 0, "!farm");
		xp[_adventurer][farm] += XP_PER_HARVEST;
		return xp[_adventurer][farm];
	}

	function getNextHarvest(uint _adventurer) external view returns (uint) {
		return nextHarvest[_adventurer][msg.sender];
	}

}

