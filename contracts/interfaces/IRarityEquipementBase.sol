// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IEquipementBase {
    function getEquipement(uint tokenId) external view returns (uint, address, address, uint8, uint8, bool);
    function equipementSlot() external view returns (uint8);
    function codexes(address) external view returns (address);
    function minters(address) external view returns (address);
    function set_equipement(
        uint _adventurer,
        address _operator,
        address _registry,
        uint256 _tokenID
    ) external;
    function set_rEquipement(
        uint _adventurer,
        uint _operator,
        address _registry,
        uint256 _tokenID
    ) external;
    function RARITY_EXTENDED_NPC() external view returns (uint);
}