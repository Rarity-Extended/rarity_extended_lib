// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityFarmBase {
    function typeOf() external view returns (uint8);
    function requiredLevel() external view returns (uint8);
}