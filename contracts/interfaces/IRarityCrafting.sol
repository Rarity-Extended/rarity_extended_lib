// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityCrafting {
    function craft(uint _adventurer, uint8 _base_type, uint8 _item_type, uint _crafting_materials) external;
    function simulate(uint _summoner, uint _base_type, uint _item_type, uint _crafting_materials) external view returns (bool crafted, int check, uint cost, uint dc);
    function transferFrom(address from, address to, uint256 tokenId) external;
    function next_item() external view returns (uint);
    function SUMMMONER_ID() external view returns (uint);
}