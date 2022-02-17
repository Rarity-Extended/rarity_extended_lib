// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";
import "../../extended.sol";
import "../../rarity.sol";
import "../../interfaces/IRarity.sol";
import "../../interfaces/IERC721.sol";
import "../../interfaces/IRarityEquipementCodexType2.sol";
import "../../interfaces/IRarityEquipementCodexType3.sol";
import "../../interfaces/IRarityEquipementSource.sol";
import "../../interfaces/IRarityEquipementWrapper.sol";
import "../../interfaces/IRarityEquipementBase.sol";

abstract contract rarity_extended_equipement_base is ERC721Holder, Extended, Rarity {
	address public equipementWrapper;
	uint8 public equipementItemType;
	uint8 public equipementSlot;
    
    event EquipementWrapperSet(address wrapper);
    event RegistrySet(address registry, address codex, address minter);
	
	//Registry -> codex, aka approved contract to get informations
    mapping(address => address) public codexes; //Registry -> codex, aka approved contract to get informations
    mapping(address => address) public minters; //Registry -> minter, aka contract from which the ERC721 or rERC721 are minted

	/*******************************************************************************
    **  @dev References aboute a specific equipement for an adventurer.
    **	@param __key__: TokenID of the adventurer
    **	@param tokenID: ID of the NFT
    **	@param registry: address of the NFT
    **	@param fromAdventurer: Is the owner an adventurer or a wallet
	*******************************************************************************/
    struct Equipement {
        uint tokenID;
        address registry;
        bool fromAdventurer;
    }
    mapping(uint => Equipement) public equipement;

	/*******************************************************************************
    **  @dev Register the abstract contract.
    **	@param _equipementItemType: Can be one of theses:
	**	- 1 for Goods
	**	- 2 for Armor
	**	- 3 for Weapons
	**	- 4 for Jewelries
    **	@param _slot: Slot to use
    **	@param _wrapper: Wrapper contract address
	*******************************************************************************/
	constructor(uint8 _equipementItemType, uint8 _slot, address _wrapper) Extended() Rarity(true) {
		equipementItemType = _equipementItemType;
		equipementSlot = _slot;
		equipementWrapper = _wrapper;
	}

	/*******************************************************************************
    **  @dev Assign an equipement to an adventurer. If the adventurer already has
	**	one, it will revert. The owner of the adventurer must be the owner of the
	**	equipement, or it must be an approve address.
    **  The ERC721 is transfered to this contract, aka locked. The player will have
	**	to unset the armor before it can be transfered to another player.
    **  @param _owner: current owner of the NFT
    **  @param _adventurer: TokenID of the adventurer we want to assign to
    **	@param _operator: Address in which name we are acting for.
    **	@param _registry: Address of the contract from which is generated the ERC721
    **	@param _tokenID: TokenID of equipement
	*******************************************************************************/
    function set_equipement(uint _adventurer, address _operator, address _registry, uint256 _tokenID) virtual public {
        address codex = codexes[_registry];
        require(codex != address(0), "!registered");
        address minter = minters[_registry];
        require(minter != address(0), "!minter");

        (uint8 base_type, uint8 item_type,,) = IEquipementSource(_registry).items(_tokenID);
        require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
        require(_isApprovedOrOwnerOfItem(_tokenID, IERC721(minter), msg.sender), "!equipement"); 
		require(base_type == equipementItemType, "!base_type");
        require(equipement[_adventurer].registry == address(0), "!already_equiped");

        _handle_specific_situations(_adventurer, codex, item_type);
        equipement[_adventurer] = Equipement(_tokenID, minter, false);
        IERC721(minter).safeTransferFrom(_operator, address(this), _tokenID);
    }

	/*******************************************************************************
    **  @notice Assign an equipement to an adventurer. If the adventurer already has
	**	one, it will revert. The owner of the adventurer must be the owner of the
	**	equipement, or it must be an approve address.
    **  The ERC721 is transfered to this contract, aka locked. The player will have
	**	to unset the armor before it can be transfered to another player.
    **  @param _adventurer: the tokenID of the adventurer to assign the armor
    **	@param _operator: adventurer in which name we are acting for.
    **	@param _registry: address of the base contract for this item, aka with
    **  which we will interact to transfer the item
    **	@param _tokenID: the tokenID of the armor
	*******************************************************************************/
    function set_rEquipement(
        uint _adventurer,
        uint _operator,
        address _registry,
        uint256 _tokenID
    ) virtual public {
        address codex = codexes[_registry];
        require(codex != address(0), "!registered");
        address minter = minters[_registry];
        require(minter != address(0), "!minter");
        uint owner = IrERC721(minter).ownerOf(_tokenID);

        (uint8 base_type, uint8 item_type,,) = IEquipementSource(_registry).items(_tokenID);
        require(_isApprovedOrOwner(owner, msg.sender), "!owner");
        require(_isApprovedOrOwnerOfItem(_tokenID, IrERC721(minter), _operator), "!equipement");
		require(base_type == equipementItemType, "!base_type");
        require(equipement[_adventurer].registry == address(0), "!already_equiped");

        _handle_specific_situations(_adventurer, codex, item_type);

        IrERC721(minter).transferFrom(
            /* operator = */ RARITY_EXTENDED_NPC,
            /* from = */ owner,
            /* to = */ RARITY_EXTENDED_NPC,
            /* id = */ _tokenID
        );
        equipement[_adventurer] = Equipement(_tokenID, minter, true);
    }

    function set_rEquipement(
        uint _adventurer,
        uint _operator,
        address _registry,
        uint256 _tokenID,
        uint256 deadline,
        bytes calldata signature
    ) virtual public {
        address codex = codexes[_registry];
        require(codex != address(0), "!registered");
        address minter = minters[_registry];
        require(minter != address(0), "!minter");
        uint owner = IrERC721(minter).ownerOf(_tokenID);

        IrERC721(minter).permit(RARITY_EXTENDED_NPC, owner, RARITY_EXTENDED_NPC, _tokenID, deadline, signature);

        (uint8 base_type, uint8 item_type,,) = IEquipementSource(_registry).items(_tokenID);
        require(_isApprovedOrOwner(owner, msg.sender), "!owner");
        require(_isApprovedOrOwnerOfItem(_tokenID, IrERC721(minter), _operator), "!equipement");
		require(base_type == equipementItemType, "!base_type");
        require(equipement[_adventurer].registry == address(0), "!already_equiped");

        _handle_specific_situations(_adventurer, codex, item_type);

        IrERC721(minter).transferFrom(
            /* operator = */ RARITY_EXTENDED_NPC,
            /* from = */ owner,
            /* to = */ RARITY_EXTENDED_NPC,
            /* id = */ _tokenID
        );
        equipement[_adventurer] = Equipement(_tokenID, minter, true);
    }

	/*******************************************************************************
    **  @dev Some equipements may require some specific verifications. Example are
    **  you cannot equip a shield if you already have two weapons, or a ranged
    **  weapon. You cannot equip a shield as an armor, or an armor as a shield. You
    **  cannot equipe a secondary weapon if you have a two handed weapon or a ranged
    **  weapon.
    **  This function MUST be modified to check the requirement for the specific
    **  slot of this contract.
    **  @notice : List of checks
    **  @param _adventurer: tokenID of the adventurer to work with
    **  @param _codex: address of the Codex containing the read informations
    **	@param _item_type: type of item to check in the Codex
	*******************************************************************************/
	function _handle_specific_situations(uint _adventurer, address _codex, uint8 _item_type) virtual internal view {}

	/*******************************************************************************
    **  @dev Remove the equipement from the equiped slot and send back the NFT to
	**	the owner. The owner can be an address or an uint.
    **  @param _adventurer: tokenID of the adventurer to work with
	*******************************************************************************/
    function unset_equipement(uint _adventurer) public {
        require(_isApprovedOrOwner(_adventurer, msg.sender), "!owner");
		
		Equipement memory equipementInfo = equipement[_adventurer];
        require(equipementInfo.registry != address(0), "!noArmor");
        equipement[_adventurer] = Equipement(0, address(0), false);

        if (equipementInfo.fromAdventurer) {
            IrERC721(equipementInfo.registry).transferFrom(
                RARITY_EXTENDED_NPC,
                RARITY_EXTENDED_NPC,
                _adventurer,
                equipementInfo.tokenID
            );
        } else {
            IERC721(equipementInfo.registry).safeTransferFrom(
                address(this),
                _rm.ownerOf(_adventurer),
                equipementInfo.tokenID
            );
        }
    }

	function getEquipement(uint _adventurer) public view returns (uint, address, address, uint8, uint8, bool) {
		Equipement memory _equipement = equipement[_adventurer];
		uint8 base_type;
		uint8 item_type;
        if (_equipement.registry != address(0)) {
			(base_type, item_type,,) = IEquipementSource(_equipement.registry).items(_equipement.tokenID);
		}
		return (
			_equipement.tokenID,
			_equipement.registry,
			codexes[_equipement.registry],
			base_type,
			item_type,
			_equipement.fromAdventurer
		);
	}

	function name() virtual public pure returns (string memory) {
		return ("Rarity Extended Equipement");
	}

	// ADMIN FUNCTIONS
	function addRegistry(address _registry, address _minter, address _codex) public onlyExtended() {
		require(codexes[_registry] == address(0), "!assigned");
		codexes[_registry] = _codex;
		minters[_registry] = _minter;

		emit RegistrySet(_registry, _codex, _minter);
	}

	function removeRegistry(address _registry) public onlyExtended() {
		require(codexes[_registry] != address(0), "!assigned");
		codexes[_registry] = address(0);
		minters[_registry] = address(0);

		emit RegistrySet(_registry, address(0), address(0));
	}

	function setEquipementWrapper(address _wrapper) public onlyExtended() {
		equipementWrapper = _wrapper;
		emit EquipementWrapperSet(_wrapper);
	}

}
