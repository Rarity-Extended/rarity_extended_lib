// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "./utils/ERC721Enumerable.sol";
import "./utils/Base64.sol";

contract rarity is ERC721Enumerable {
    uint public next_summoner;
    uint constant xp_per_day = 250e18;
    uint constant DAY = 1 days;

    string constant name = "Rarity Manifested";
    string constant symbol = "RM";

    mapping(uint => uint) public xp;
    mapping(uint => uint) public adventurers_log;
    mapping(uint => uint) public class;
    mapping(uint => uint) public level;

    event summoned(address indexed owner, uint class, uint summoner);
    event leveled(address indexed owner, uint level, uint summoner);

    function adventure(uint _summoner) external {
        require(_isApprovedOrOwner(msg.sender, _summoner));
        require(block.timestamp > adventurers_log[_summoner]);
        adventurers_log[_summoner] = block.timestamp + DAY;
        xp[_summoner] += xp_per_day;
    }

    function spend_xp(uint _summoner, uint _xp) external {
        require(_isApprovedOrOwner(msg.sender, _summoner));
        xp[_summoner] -= _xp;
    }

    function level_up(uint _summoner) external {
        require(_isApprovedOrOwner(msg.sender, _summoner));
        uint _level = level[_summoner];
        uint _xp_required = xp_required(_level);
        xp[_summoner] -= _xp_required;
        level[_summoner] = _level+1;
        emit leveled(msg.sender, level[_summoner], _summoner);
    }

    function summoner(uint _summoner) external view returns (uint _xp, uint _log, uint _class, uint _level) {
        _xp = xp[_summoner];
        _log = adventurers_log[_summoner];
        _class = class[_summoner];
        _level = level[_summoner];
    }

    function summon(uint _class) external {
        require(1 <= _class && _class <= 11);
        uint _next_summoner = next_summoner;
        class[_next_summoner] = _class;
        level[_next_summoner] = 1;
        _safeMint(msg.sender, _next_summoner);
        emit summoned(msg.sender, _class, _next_summoner);
        next_summoner++;
    }

    function xp_required(uint curent_level) public pure returns (uint xp_to_next_level) {
        xp_to_next_level = curent_level * 1000e18;
        for (uint i = 1; i < curent_level; i++) {
            xp_to_next_level += curent_level * 1000e18;
        }
    }

    function tokenURI(uint256 _summoner) public view returns (string memory) {
        string[7] memory parts;
        parts[0] = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 350 350"><style>.base { fill: white; font-family: serif; font-size: 14px; }</style><rect width="100%" height="100%" fill="black" /><text x="10" y="20" class="base">';

        parts[1] = string(abi.encodePacked("class", " ", classes(class[_summoner])));

        parts[2] = '</text><text x="10" y="40" class="base">';

        parts[3] = string(abi.encodePacked("level", " ", toString(level[_summoner])));

        parts[4] = '</text><text x="10" y="60" class="base">';

        parts[5] = string(abi.encodePacked("xp", " ", toString(xp[_summoner]/1e18)));

        parts[6] = '</text></svg>';

        string memory output = string(abi.encodePacked(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]));

        string memory json = Base64.encode(bytes(string(abi.encodePacked('{"name": "summoner #', toString(_summoner), '", "description": "Rarity is achieved via an active economy, summoners must level, gain feats, learn spells, to be able to craft gear. This allows for market driven rarity while allowing an ever growing economy. Feats, spells, and summoner gear is ommitted as part of further expansions.", "image": "data:image/svg+xml;base64,', Base64.encode(bytes(output)), '"}'))));
        output = string(abi.encodePacked('data:application/json;base64,', json));

        return output;
    }

    function classes(uint id) public pure returns (string memory description) {
        if (id == 1) {
            return "Barbarian";
        } else if (id == 2) {
            return "Bard";
        } else if (id == 3) {
            return "Cleric";
        } else if (id == 4) {
            return "Druid";
        } else if (id == 5) {
            return "Fighter";
        } else if (id == 6) {
            return "Monk";
        } else if (id == 7) {
            return "Paladin";
        } else if (id == 8) {
            return "Ranger";
        } else if (id == 9) {
            return "Rogue";
        } else if (id == 10) {
            return "Sorcerer";
        } else if (id == 11) {
            return "Wizard";
        }
    }

    function toString(uint256 value) internal pure returns (string memory) {
    // Inspired by OraclizeAPI's implementation - MIT license
    // https://github.com/oraclize/ethereum-api/blob/b42146b063c7d6ee1358846c198246239e9360e8/oraclizeAPI_0.4.25.sol

        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
}
