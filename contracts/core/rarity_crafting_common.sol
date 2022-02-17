// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "./utils/ERC721Enumerable.sol";
import "./utils/Base64.sol";

interface rarity {
    function level(uint) external view returns (uint);
    function getApproved(uint) external view returns (address);
    function ownerOf(uint) external view returns (address);
    function class(uint) external view returns (uint);
    function summon(uint _class) external;
    function next_summoner() external view returns (uint);
    function spend_xp(uint _summoner, uint _xp) external;
}

interface rarity_attributes {
    function character_created(uint) external view returns (bool);
    function ability_scores(uint) external view returns (uint32,uint32,uint32,uint32,uint32,uint32);
}

interface rarity_skills {
    function get_skills(uint _summoner) external view returns (uint8[36] memory);
}

interface rarity_gold {
    function transferFrom(uint executor, uint from, uint to, uint amount) external returns (bool);
}

interface rarity_crafting_materials_i {
    function transferFrom(uint executor, uint from, uint to, uint amount) external returns (bool);
}

interface codex_items_goods {
    function item_by_id(uint _id) external pure returns(
        uint id,
        uint cost,
        uint weight,
        string memory name,
        string memory description
    );
}

interface codex_items_armor {
    function get_proficiency_by_id(uint _id) external pure returns (string memory description);
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

interface codex_items_weapons {
    struct weapon {
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

    function get_proficiency_by_id(uint _id) external pure returns (string memory description);
    function get_encumbrance_by_id(uint _id) external pure returns (string memory description);
    function get_damage_type_by_id(uint _id) external pure returns (string memory description);
    function item_by_id(uint _id) external pure returns(weapon memory _weapon);
}

interface codex_base_random {
    function d20(uint _summoner) external view returns (uint);
}

contract rarity_crafting is ERC721Enumerable {
    uint public next_item;
    uint constant craft_xp_per_day = 250e18;

    rarity constant _rm = rarity(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    rarity_attributes constant _attr = rarity_attributes(0xB5F5AF1087A8DA62A23b08C00C6ec9af21F397a1);
    rarity_crafting_materials_i constant _craft_i = rarity_crafting_materials_i(0x2A0F1cB17680161cF255348dDFDeE94ea8Ca196A);
    rarity_gold constant _gold = rarity_gold(0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2);
    rarity_skills constant _skills = rarity_skills(0x51C0B29A1d84611373BA301706c6B4b72283C80F);

    codex_base_random constant _random = codex_base_random(0x7426dBE5207C2b5DaC57d8e55F0959fcD99661D4);
    codex_items_goods constant _goods = codex_items_goods(0x0C5C1CC0A7AE65FE372fbb08FF16578De4b980f3);
    codex_items_armor constant _armor = codex_items_armor(0xf5114A952Aca3e9055a52a87938efefc8BB7878C);
    codex_items_weapons constant _weapons = codex_items_weapons(0xeE1a2EA55945223404d73C0BbE57f540BBAAD0D8);

    string constant public name = "Rarity Crafting (I)";
    string constant public symbol = "RC(I)";

    event Crafted(address indexed owner, uint check, uint summoner, uint base_type, uint item_type, uint gold, uint craft_i);

    uint public immutable SUMMMONER_ID;

    constructor() {
        SUMMMONER_ID = _rm.next_summoner();
        _rm.summon(11);
    }

    struct item {
        uint8 base_type;
        uint8 item_type;
        uint32 crafted;
        uint crafter;
    }

    function _isApprovedOrOwner(uint _summoner) internal view returns (bool) {
        return _rm.getApproved(_summoner) == msg.sender || _rm.ownerOf(_summoner) == msg.sender;
    }

    function get_goods_dc() public pure returns (uint dc) {
        return 20;
    }

    function get_armor_dc(uint _item_id) public pure returns (uint dc) {
        (,,,,uint _armor_bonus,,,,,) = _armor.item_by_id(_item_id);
        return 20 + _armor_bonus;
    }

    function get_weapon_dc(uint _item_id) public pure returns (uint dc) {
        codex_items_weapons.weapon memory _weapon = _weapons.item_by_id(_item_id);
        if (_weapon.proficiency == 1) {
            return 20;
        } else if (_weapon.proficiency == 2) {
            return 25;
        } else if (_weapon.proficiency == 3) {
            return 30;
        }
    }

    function get_dc(uint _base_type, uint _item_id) public pure returns (uint dc) {
        if (_base_type == 1) {
            return get_goods_dc();
        } else if (_base_type == 2) {
            return get_armor_dc(_item_id);
        } else if (_base_type == 3) {
            return get_weapon_dc(_item_id);
        }
    }

    function get_item_cost(uint _base_type, uint _item_type) public pure returns (uint cost) {
        if (_base_type == 1) {
            (,cost,,,) = _goods.item_by_id(_item_type);
        } else if (_base_type == 2) {
            (,cost,,,,,,,,) = _armor.item_by_id(_item_type);
        } else if (_base_type == 3) {
            codex_items_weapons.weapon memory _weapon = _weapons.item_by_id(_item_type);
            cost = _weapon.cost;
        }
    }

    function modifier_for_attribute(uint _attribute) public pure returns (int _modifier) {
        if (_attribute == 9) {
            return -1;
        }
        return (int(_attribute) - 10) / 2;
    }

    function craft_skillcheck(uint _summoner, uint _dc) public view returns (bool crafted, int check) {
        check = int(uint(_skills.get_skills(_summoner)[5]));
        if (check == 0) {
            return (false, 0);
        }
        (,,,uint _int,,) = _attr.ability_scores(_summoner);
        check += modifier_for_attribute(_int);
        if (check <= 0) {
            return (false, 0);
        }
        check += int(_random.d20(_summoner));
        return (check >= int(_dc), check);
    }

    function isValid(uint _base_type, uint _item_type) public pure returns (bool) {
        if (_base_type == 1) {
            return (1 <= _item_type && _item_type <= 24);
        } else if (_base_type == 2) {
            return (1 <= _item_type && _item_type <= 18);
        } else if (_base_type == 3) {
            return (1 <= _item_type && _item_type <= 59);
        }
        return false;
    }

    function simulate(uint _summoner, uint _base_type, uint _item_type, uint _crafting_materials) external view returns (bool crafted, int check, uint cost, uint dc) {
        dc = get_dc(_base_type, _item_type);
        if (_crafting_materials >= 10) {
            dc = dc - (_crafting_materials / 10);
        }
        (crafted, check) = craft_skillcheck(_summoner, dc);
        if (crafted) {
            cost = get_item_cost(_base_type, _item_type);
        }
    }

    function craft(uint _summoner, uint8 _base_type, uint8 _item_type, uint _crafting_materials) external {
        require(_isApprovedOrOwner(_summoner), "!owner");
        require(_attr.character_created(_summoner), "!created");
        require(_summoner != SUMMMONER_ID, "hax0r");
        require(isValid(_base_type, _item_type), "!valid");
        uint _dc = get_dc(_base_type, _item_type);
        if (_crafting_materials >= 10) {
            require(_craft_i.transferFrom(SUMMMONER_ID, _summoner, SUMMMONER_ID, _crafting_materials), "!craft");
            _dc = _dc - (_crafting_materials / 10);
        }
        (bool crafted, int check) = craft_skillcheck(_summoner, _dc);
        if (crafted) {
            uint _cost = get_item_cost(_base_type, _item_type);
            require(_gold.transferFrom(SUMMMONER_ID, _summoner, SUMMMONER_ID, _cost), "!gold");
            items[next_item] = item(_base_type, _item_type, uint32(block.timestamp), _summoner);
            _safeMint(msg.sender, next_item);
            emit Crafted(msg.sender, uint(check), _summoner, _base_type, _item_type, _cost, _crafting_materials);
            next_item++;
        }
        _rm.spend_xp(_summoner, craft_xp_per_day);
    }

    mapping(uint => item) public items;

    function get_type(uint _type_id) public pure returns (string memory _type) {
        if (_type_id == 1) {
            _type = "Goods";
        } else if (_type_id == 2) {
            _type = "Armor";
        } else if (_type_id == 3) {
            _type = "Weapons";
        }
    }

    function tokenURI(uint _item) public view returns (string memory uri) {
        uint _base_type = items[_item].base_type;
        if (_base_type == 1) {
            return get_token_uri_goods(_item);
        } else if (_base_type == 2) {
            return get_token_uri_armor(_item);
        } else if (_base_type == 3) {
            return get_token_uri_weapon(_item);
        }
    }

    function get_token_uri_goods(uint _item) public view returns (string memory output) {
        item memory _data = items[_item];
        {
            (,
                uint _cost,
                uint _weight,
                string memory _name,
                string memory _description
            ) = _goods.item_by_id(_data.item_type);
            output = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 350 350"><style>.base { fill: white; font-family: serif; font-size: 14px; }</style><rect width="100%" height="100%" fill="black" /><text x="10" y="20" class="base">';
            output = string(abi.encodePacked(output, "category ", get_type(_data.base_type), '</text><text x="10" y="40" class="base">'));
            output = string(abi.encodePacked(output, "name ", _name, '</text><text x="10" y="60" class="base">'));
            output = string(abi.encodePacked(output, "cost ", toString(_cost/1e18), "gp", '</text><text x="10" y="80" class="base">'));
            output = string(abi.encodePacked(output, "weight ", toString(_weight), "lb", '</text><text x="10" y="100" class="base">'));
            output = string(abi.encodePacked(output, "description ", _description, '</text><text x="10" y="120" class="base">'));
            output = string(abi.encodePacked(output, "crafted by ", toString(_data.crafter), '</text><text x="10" y="140" class="base">'));
            output = string(abi.encodePacked(output, "crafted at ", toString(_data.crafted), '</text></svg>'));
        }
        output = string(abi.encodePacked('data:application/json;base64,', Base64.encode(bytes(string(abi.encodePacked('{"name": "item #', toString(_item), '", "description": "Rarity tier 1, non magical, item crafting.", "image": "data:image/svg+xml;base64,', Base64.encode(bytes(output)), '"}'))))));

        return output;
    }

    function get_token_uri_armor(uint _item) public view returns (string memory output) {
        item memory _data = items[_item];
        {
            (,
                uint _cost,
                uint _proficiency,
                uint _weight,
                uint _armor_bonus,
                uint _max_dex_bonus,
                int _penalty,
                uint _spell_failure,
                string memory _name,
                string memory _description
            ) = _armor.item_by_id(_data.item_type);
            output = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 350 350"><style>.base { fill: white; font-family: serif; font-size: 14px; }</style><rect width="100%" height="100%" fill="black" /><text x="10" y="20" class="base">';
            output = string(abi.encodePacked(output, "category ", get_type(_data.base_type), '</text><text x="10" y="40" class="base">'));
            output = string(abi.encodePacked(output, "name ", _name, '</text><text x="10" y="60" class="base">'));
            output = string(abi.encodePacked(output, "cost ", toString(_cost/1e18), "gp", '</text><text x="10" y="80" class="base">'));
            output = string(abi.encodePacked(output, "weight ", toString(_weight), "lb", '</text><text x="10" y="100" class="base">'));
            output = string(abi.encodePacked(output, "proficiency ", _armor.get_proficiency_by_id(_proficiency), '</text><text x="10" y="120" class="base">'));
            output = string(abi.encodePacked(output, "armor bonus ", toString(_armor_bonus), '</text><text x="10" y="140" class="base">'));
            output = string(abi.encodePacked(output, "max dex ", toString(_max_dex_bonus), '</text><text x="10" y="160" class="base">'));
            output = string(abi.encodePacked(output, "penalty ", toString(_penalty), '</text><text x="10" y="180" class="base">'));
            output = string(abi.encodePacked(output, "spell failure ", toString(_spell_failure), "%", '</text><text x="10" y="200" class="base">'));
            output = string(abi.encodePacked(output, "description ", _description, '</text><text x="10" y="220" class="base">'));
            output = string(abi.encodePacked(output, "crafted by ", toString(_data.crafter), '</text><text x="10" y="240" class="base">'));
            output = string(abi.encodePacked(output, "crafted at ", toString(_data.crafted), '</text></svg>'));
        }
        output = string(abi.encodePacked('data:application/json;base64,', Base64.encode(bytes(string(abi.encodePacked('{"name": "item #', toString(_item), '", "description": "Rarity tier 1, non magical, item crafting.", "image": "data:image/svg+xml;base64,', Base64.encode(bytes(output)), '"}'))))));
    }

    function get_token_uri_weapon(uint _item) public view returns (string memory output) {
        item memory _data = items[_item];
        {
            codex_items_weapons.weapon memory _weapon = _weapons.item_by_id(_data.item_type);
            output = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 350 350"><style>.base { fill: white; font-family: serif; font-size: 14px; }</style><rect width="100%" height="100%" fill="black" /><text x="10" y="20" class="base">';
            output = string(abi.encodePacked(output, "category ", get_type(_data.base_type), '</text><text x="10" y="40" class="base">'));
            output = string(abi.encodePacked(output, "name ", _weapon.name, '</text><text x="10" y="60" class="base">'));
            output = string(abi.encodePacked(output, "cost ", toString(_weapon.cost/1e18), "gp", '</text><text x="10" y="80" class="base">'));
            output = string(abi.encodePacked(output, "weight ", toString(_weapon.weight), "lb", '</text><text x="10" y="100" class="base">'));
            output = string(abi.encodePacked(output, "proficiency ", _weapons.get_proficiency_by_id(_weapon.proficiency), '</text><text x="10" y="120" class="base">'));
            output = string(abi.encodePacked(output, "encumbrance ", _weapons.get_encumbrance_by_id(_weapon.encumbrance), '</text><text x="10" y="140" class="base">'));
            output = string(abi.encodePacked(output, "damage 1d", toString(_weapon.damage), " ", _weapons.get_damage_type_by_id(_weapon.damage_type), '</text><text x="10" y="160" class="base">'));
            output = string(abi.encodePacked(output, "(modifier) x critical (", toString(_weapon.critical_modifier), ") x ", toString(_weapon.critical), '</text><text x="10" y="180" class="base">'));
            output = string(abi.encodePacked(output, "range ", toString(_weapon.range_increment), "ft", '</text><text x="10" y="200" class="base">'));
            output = string(abi.encodePacked(output, "description ", _weapon.description, '</text><text x="10" y="220" class="base">'));
            output = string(abi.encodePacked(output, "crafted by ", toString(_data.crafter), '</text><text x="10" y="240" class="base">'));
            output = string(abi.encodePacked(output, "crafted at ", toString(_data.crafted), '</text></svg>'));
        }
        output = string(abi.encodePacked('data:application/json;base64,', Base64.encode(bytes(string(abi.encodePacked('{"name": "item #', toString(_item), '", "description": "Rarity tier 1, non magical, item crafting.", "image": "data:image/svg+xml;base64,', Base64.encode(bytes(output)), '"}'))))));
    }

    function toString(int value) internal pure returns (string memory) {
        string memory _string = '';
        if (value < 0) {
            _string = '-';
            value = value * -1;
        }
        return string(abi.encodePacked(_string, toString(uint(value))));
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
