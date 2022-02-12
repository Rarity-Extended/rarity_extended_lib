// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "../extended.sol";
import "../rarity.sol";
import "../interfaces/IRarityEquipementBase.sol";

contract rarity_extended_equipement_wrapper is Extended {
    string constant public name  = "Rarity Extended Equipement Wrapper";
        
	constructor() Extended() {}

	//Slot -> Equipement contract
    mapping(uint => address) public slots;

	/*******************************************************************************
    **  @dev Assign a new equipement contract to a slot index. As time of deployment
    **  slots are: 
    **  - 0 -> undefined
    **  - 1 -> Head armor (helmet, hats)
    **  - 2 -> Body armor (plate armor, leather, robe)
    **  - 3 -> Hand armor (gloves and gantelet. No weapons gantelet)
    **  - 4 -> Foot armor (boots and sabatons)
    **  - 5 -> Primary weapon
    **  - 6 -> Secondary weapon
    **  - 7 -> First Jewelry 
    **  - 8 -> Second jewelry
    **  Some slot are virtual like shield (assigned to secondary weapon)
    **  - 101 -> shield
    **	@param _equipement: Address of the contract handling the equipement
	*******************************************************************************/
    function registerSlot(address _equipement) public onlyExtended() {
        require(_equipement != address(0), "!equipement");
        uint8 _slot = IEquipementBase(_equipement).equipementSlot();
        require(_slot != 0, "!slot");
        require(slots[_slot] == address(0), '!new');
        slots[_slot] = _equipement;
    }

    /*******************************************************************************
    **  @dev Retrieve a specific equipement by it's slot
    **	@param _adventurer: tokenID of the adventurer we want to get the equipement
    **  @param _slot: ID of the slot we want to assign to
    *******************************************************************************/
    function getEquipementBySlot(uint _adventurer, uint _slot) public view returns (
        uint tokenID,
        address registry,
        address codex,
        uint8 base_type,
        uint8 item_type,
        bool fromAdventurer
    ) {
        (tokenID, registry, codex, base_type, item_type, fromAdventurer) = IEquipementBase(slots[_slot]).getEquipement(_adventurer);
    }

}
