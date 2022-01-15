// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRaritySkinManager {
    struct Skin {
        address implementation;
        uint256 tokenId;
    }
    function skinOf(uint summoner) external view returns (Skin memory);
}