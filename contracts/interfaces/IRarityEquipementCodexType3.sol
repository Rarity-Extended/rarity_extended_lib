// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IEquipementCodexType3 {
    struct Item {
        uint id;
        uint cost;
        uint proficiency;
        uint encumbrance;
        uint damage_type;
        uint weight;
        uint damage;
        uint critical;
        int critical_modifier;
        uint range_increment;
        string name;
        string description;
    }
    function item_by_id(uint _id) external pure returns(Item memory _weapon);
}
