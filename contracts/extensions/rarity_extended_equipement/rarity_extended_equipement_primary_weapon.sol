// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./rarity_extended_equipement_base.sol";

contract rarity_extended_equipement_primary_weapon is rarity_extended_equipement_base {
	constructor(uint8 _equipementItemType, uint8 _slot, address _wrapper)
        rarity_extended_equipement_base(_equipementItemType, _slot, _wrapper) {
	}

	function name() override public pure returns (string memory) {
		return ("Rarity Extended Equipement Primary Weapon");
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
    **  - Check if a secondary weapon is equiped while new weapon is two handed
    **  - Check if a secondary weapon is equiped while new weapon is ranged
    **  - Check if a shield is equiped while new weapon is two handed
    **  - Check if a shield is equiped while new weapon is ranged
    **  @param _adventurer: tokenID of the adventurer to work with
    **  @param _codex: address of the Codex containing the read informations
    **	@param _item_type: type of item to check in the Codex
	*******************************************************************************/
    function _handle_specific_situations(uint _adventurer, address _codex, uint8 _item_type) override internal view {
        // Check that the item is indeed a shield
        IEquipementCodexType3.Item memory item = IEquipementCodexType3(_codex).item_by_id(_item_type);
        if (item.encumbrance >= 4) {
            // Check that no secondary weapon is equiped
            (,address registrySecWeapon,,,,) = IEquipementWrapper(equipementWrapper).getEquipementBySlot(_adventurer, 6);
            require(registrySecWeapon == address(0), '!secondary_weapon');

            // Check that no shield is equiped
            (,address registryShield,,,,) = IEquipementWrapper(equipementWrapper).getEquipementBySlot(_adventurer, 101);
            require(registryShield == address(0), '!shield');
        }
    }
}
