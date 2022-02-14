// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./rarity_extended_equipement_base.sol";

contract rarity_extended_equipement_secondary_weapon is rarity_extended_equipement_base {
	constructor(uint8 _equipementItemType, uint8 _slot, address _wrapper)
        rarity_extended_equipement_base(_equipementItemType, _slot, _wrapper) {
	}

	function name() override public pure returns (string memory) {
		return ("Rarity Extended Equipement Secondary Weapon");
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
    **  - Check if a equipement is not two handed/ranged
    **  - Check if a two handed primary weapon is equiped
    **  - Check if a ranged primary weapon is equiped
    **  - Check if a shield is already equiped
    **  @param _adventurer: tokenID of the adventurer to work with
    **  @param _codex: address of the Codex containing the read informations
    **	@param _item_type: type of item to check in the Codex
	*******************************************************************************/
    function _handle_specific_situations(uint _adventurer, address _codex, uint8 _item_type) override internal view {
        // Check that the item is not two handed/ranged
        IEquipementCodexType3.Item memory item = IEquipementCodexType3(_codex).item_by_id(_item_type);
        require(item.encumbrance < 4, '!encumbrance');

        // Check that no shield is equiped
        (,address registryShield,,,,) = IEquipementWrapper(equipementWrapper).getEquipementBySlot(_adventurer, 101);
        require(registryShield == address(0), '!shield');

        // Check that no primary twohanded/ranger weapon is equiped
        (,address registryPrimWeapon, address codexPrimWeapon,,uint8 item_type,) = IEquipementWrapper(equipementWrapper).getEquipementBySlot(_adventurer, 5);
        if (registryPrimWeapon != address(0)) {
            IEquipementCodexType3.Item memory _weapon = IEquipementCodexType3(codexPrimWeapon).item_by_id(item_type);
            require(_weapon.encumbrance < 4, "!primary_encumbrance");
        }
    }
}
