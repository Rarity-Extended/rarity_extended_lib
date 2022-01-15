// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRaritySkin {
    function tokenURI(uint256 _tokenId) external view returns (string memory);
}