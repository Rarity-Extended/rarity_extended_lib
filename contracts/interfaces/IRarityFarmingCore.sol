// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityFarmingCore {
    function xp(uint _adventurer, uint _farmType) external view returns (uint);
    function level(uint _adventurer, uint _farmType) external view returns (uint);
	function earnXp(uint _adventurer) external returns (uint);
}