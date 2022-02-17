// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./rarity_extended_equipement_base.sol";

contract rarity_extended_equipement_armor_body is rarity_extended_equipement_base {
	constructor(uint8 _equipementItemType, uint8 _slot, address _wrapper)
        rarity_extended_equipement_base(_equipementItemType, _slot, _wrapper) {
	}

	function name() override public pure returns (string memory) {
		return ("Rarity Extended Equipement Armor Body");
	}

	/*******************************************************************************
    **  @dev Some equipements may require some specific verifications. Example are
    **  you cannot equip a shield if you already have two weapons, or a ranged
    **  weapon. You cannot equip a shield as an armor, or an armor as a shield. You
    **  cannot equipe a secondary weapon if you have a two handed weapon or a ranged
    **  weapon.
    **  This function MUST be modified to check the requirement for the specific
    **  slot of this contract.
    **  @notice :
    **  - Check if the armor is not a shield
    **  @param _adventurer: tokenID of the adventurer to work with
    **  @param _codex: address of the Codex containing the read informations
    **	@param _item_type: type of item to check in the Codex
	*******************************************************************************/
    function _handle_specific_situations(uint _adventurer, address _codex, uint8 _item_type) override internal pure {
        // Check that the item is not a shield
        (,,uint proficiency,,,,,,,) = IEquipementCodexType2(_codex).item_by_id(_item_type);
        require(proficiency != 4, '!shield');

        _adventurer; //quiet please
    }
}
