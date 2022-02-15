// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./rarity_extended_equipement_base.sol";

contract rarity_extended_equipement_shield is rarity_extended_equipement_base {
	constructor(uint8 _equipementItemType, uint8 _slot, address _wrapper)
        rarity_extended_equipement_base(_equipementItemType, _slot, _wrapper) {
	}

    function name() override public pure returns (string memory) {
		return ("Rarity Extended Equipement Shield");
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
    **  - Check if the proficiency of the armor we got is 4 (aka shield)
    **  - Check if a two handed weapon is equiped
    **  - Check if a ranged weapon is equiped
    **  - Check if a secondary weapon is equiped
    **  @param _adventurer: tokenID of the adventurer to work with
    **  @param _codex: address of the Codex containing the read informations
    **	@param _item_type: type of item to check in the Codex
	*******************************************************************************/
    function _handle_specific_situations(uint _adventurer, address _codex, uint8 _item_type) override internal view {
        // Check that the item is indeed a shield
        (,,uint proficiency,,,,,,,) = IEquipementCodexType2(_codex).item_by_id(_item_type);
        require(proficiency == 4, '!shield');
    
        // Check that no secondary weapon is equiped
        (,address registrySecWeapon,,,,) = IEquipementWrapper(equipementWrapper).getEquipementBySlot(_adventurer, 6);
        require(registrySecWeapon == address(0), '!secondary_weapon');

        // Check that no primary twohanded/ranger weapon is equiped
        (, address registryPrimWeapon, address codexPrimWeapon,, uint8 item_type,) = IEquipementWrapper(equipementWrapper).getEquipementBySlot(_adventurer, 5);
        if (registryPrimWeapon != address(0)) {
            IEquipementCodexType3.Item memory _weapon = IEquipementCodexType3(codexPrimWeapon).item_by_id(item_type);
            require(_weapon.encumbrance < 4, "!primary_encumbrance");
        }
    }

}
