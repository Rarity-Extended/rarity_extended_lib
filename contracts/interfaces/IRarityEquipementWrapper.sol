// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IEquipementWrapper {
    function getEquipementBySlot(uint _adventurer, uint _slot) external view returns (uint, address, address, uint8, uint8, bool);
}