// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityName {
    function summoner_name(uint summoner) external view returns (string memory name);
}