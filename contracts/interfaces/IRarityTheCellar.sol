// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityTheCellar {
    function adventure(uint _summoner) external;
    function scout(uint _summoner) external view returns (uint reward);
    function adventurers_log(uint adventurer) external view returns (uint);
}