// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityGold {
    function claimable(uint summoner) external view returns (uint amount);
    function claim(uint summoner) external;
}