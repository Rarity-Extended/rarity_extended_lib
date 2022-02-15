// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IEquipementCodexType2 {
    function item_by_id(uint _id) external pure returns(
        uint id,
        uint cost,
        uint proficiency,
        uint weight,
        uint armor_bonus,
        uint max_dex_bonus,
        int penalty,
        uint spell_failure,
        string memory name,
        string memory description
    );
}
