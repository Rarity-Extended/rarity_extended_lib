// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarity {
    function adventure(uint _summoner) external;
    function xp(uint _summoner) external view returns (uint);
    function spend_xp(uint _summoner, uint _xp) external;
    function level(uint _summoner) external view returns (uint);
    function level_up(uint _summoner) external;
    function adventurers_log(uint adventurer) external view returns (uint);
    function approve(address to, uint256 tokenId) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function ownerOf(uint _summoner) external view returns (address);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
    function next_summoner() external view returns (uint);
    function summon(uint _class) external;
}