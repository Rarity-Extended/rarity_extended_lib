// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "./rERC20.sol";

contract Loot is rERC20 {
    constructor(string memory name, string memory symbol) rERC20(name, symbol) {}
}