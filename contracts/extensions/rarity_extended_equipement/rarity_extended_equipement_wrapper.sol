// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "../../extended.sol";
import "../../rarity.sol";
import "../../interfaces/IRarityEquipementBase.sol";
import "../../interfaces/IRarityEquipementSource.sol";

contract rarity_extended_equipement_wrapper is ERC721Holder, Extended, Rarity {
    string constant public name  = "Rarity Extended Equipement Wrapper";
        
	constructor() Extended() Rarity(true) {}

	//Slot -> Equipement contract
    mapping(uint => address) public slots;

	/*******************************************************************************
    **  @notice Indicate the name of the slot
    **	@param _id: index of the slot we want to get the name
	*******************************************************************************/
    function getSlotNameByID(uint8 _id) public pure returns (string memory) {
        if (_id == 1) return ("Head armor");
        if (_id == 2) return ("Body armor");
        if (_id == 3) return ("Hand armor");
        if (_id == 4) return ("Foot armor");
        if (_id == 5) return ("Primary weapon");
        if (_id == 6) return ("Secondary weapon");
        if (_id == 7) return ("First Jewelry");
        if (_id == 8) return ("Second Jewelry");
        if (_id == 101) return ("Shields");
        return ("");
        
    }

	/*******************************************************************************
    **  @notice Assign a new equipement contract to a slot index. As time of deployment
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
        _rm.setApprovalForAll(slots[_slot], true);
    }

    /*******************************************************************************
    **  @notice Clean a slot, remove approvals
    **  @param _slot: ID of the slot we want to clean
    *******************************************************************************/
    function cleanSlot(uint _slot) public onlyExtended() {
        require(_slot != 0, "!slot");
        slots[_slot] = address(0);
        _rm.setApprovalForAll(slots[_slot], false);
    }

    /*******************************************************************************
    **  @notice Retrieve a specific equipement by it's slot
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


    /*******************************************************************************
    **  @notice Assign an equipement to an adventurer. If the adventurer already has
	**	one, it will revert. The owner of the adventurer must be the owner of the
	**	equipement, or it must be an approve address.
    **  The ERC721 is transfered to this contract, aka locked. The player will have
	**	to unset the armor before it can be transfered to another player.
    **  To unset the equipement, the equipement contract must be used
    **  @param _slot: Id of the slot we want to use
    **  @param _adventurer: the tokenID of the adventurer to assign the armor
    **	@param _operator: adventurer in which name we are acting for.
    **	@param _registry: address of the base contract for this item, aka with
    **  which we will interact to transfer the item
    **	@param _tokenID: the tokenID of the armor
	*******************************************************************************/
    function set_rEquipement(
        uint _slot,
        uint _adventurer,
        uint _operator,
        address _registry,
        uint256 _tokenID
    ) public {
        require(slots[_slot] != address(0), '!exist');
        IEquipementBase equipementSlot = IEquipementBase(slots[_slot]);
        IrERC721 minter = IrERC721(equipementSlot.minters(_registry));
        require(address(minter) != address(0), "!minter");
        require(equipementSlot.codexes(_registry) != address(0), "!registered");
        require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
        require(_isApprovedOrOwnerOfItem(_tokenID, minter, _operator), "!equipement");

        minter.transferFrom(
            RARITY_EXTENDED_NPC,
            _adventurer,
            RARITY_EXTENDED_NPC,
            _tokenID
        );
        minter.approve(
            RARITY_EXTENDED_NPC,
            equipementSlot.RARITY_EXTENDED_NPC(),
            _tokenID
        );
        equipementSlot.set_rEquipement(
            _adventurer,
            RARITY_EXTENDED_NPC,
            _registry,
            _tokenID
        );
    }

    /*******************************************************************************
    **  @notice Assign an equipement to an adventurer. If the adventurer already has
	**	one, it will revert. The owner of the adventurer must be the owner of the
	**	equipement, or it must be an approve address.
    **  The ERC721 is transfered to this contract, aka locked. The player will have
	**	to unset the armor before it can be transfered to another player.
    **  @param _adventurer: TokenID of the adventurer we want to assign to
    **	@param _operator: Address in which name we are acting for.
    **	@param _registry: Address of the contract from which is generated the ERC721
    **	@param _tokenID: TokenID of equipement
	*******************************************************************************/
    function set_equipement(
        uint _slot,
        uint _adventurer,
        address _operator,
        address _registry,
        uint256 _tokenID
    ) public {
        require(slots[_slot] != address(0), '!exist');
        IEquipementBase equipementSlot = IEquipementBase(slots[_slot]);
        IERC721 minter = IERC721(equipementSlot.minters(_registry));
        require(address(minter) != address(0), "!minter");
        require(equipementSlot.codexes(_registry) != address(0), "!registered");
        require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
        require(_isApprovedOrOwnerOfItem(_tokenID, IERC721(_registry), msg.sender), "!equipement"); 

        minter.safeTransferFrom(
            _operator,
            address(this),
            _tokenID
        );
        minter.approve(
            address(equipementSlot),
            _tokenID
        );
        equipementSlot.set_equipement(
            _adventurer,
            address(this),
            _registry,
            _tokenID
        );
    }
}
