// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IEquipementBase {
    function getEquipement(uint tokenId) external view returns (uint, address, address, uint8, uint8, bool);
    function equipementSlot() external view returns (uint8);
}