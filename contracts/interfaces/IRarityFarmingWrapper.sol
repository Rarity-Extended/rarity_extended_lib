// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityFarmingWrapper {
    function xp(uint _adventurer, uint _farmType) external view returns (uint);
    function level(uint _adventurer, uint _farmType) external view returns (uint);
	function getNextHarvest(uint _adventurer) external view returns (uint);
	function setNextHarvest(uint _adventurer, uint _delay) external returns (uint);
	function setXp(uint _adventurer) external returns (uint);
}