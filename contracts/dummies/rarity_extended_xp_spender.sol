// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

interface IRarityXPProxy {
    function spend_xp(uint adventurer, uint amount) external returns (bool);
}

contract dummy_rarity_extended_xp_spender {
    IRarityXPProxy _xp;

    constructor(address _xpProxyAddress) {
        _xp = IRarityXPProxy(_xpProxyAddress);
    }

    function spendXP(uint _summoner, uint256 _amount) external {
        _xp.spend_xp(_summoner, _amount);
    }
}