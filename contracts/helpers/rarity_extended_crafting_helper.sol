// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "../interfaces/IRarity.sol";
import "../interfaces/IrERC20.sol";
import "../interfaces/IRarityCrafting.sol";

contract rarity_extended_crafting_helper is IERC721Receiver {
    string constant public name = "Rarity Extended Crafting Helper";

    // Define the list of addresse we will need to interact with
    IRarity constant _rm = IRarity(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    IrERC20 constant _rarityCraftingMaterials = IrERC20(0x2A0F1cB17680161cF255348dDFDeE94ea8Ca196A);
    IrERC20 constant _rarityGold = IrERC20(0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2);
    IRarityCrafting constant _rarityCrafting = IRarityCrafting(0xf41270836dF4Db1D28F7fd0935270e3A603e78cC);
    uint constant RARITY_CRAFTING_SUMMMONER_ID = 1758709; //NPC of the RarityCrafting contract

    struct Item {
        uint8 base_type;
        uint8 item_type;
        uint256 crafter;
        uint256 item_id;
    }

    mapping(uint => uint) public expected;

    /**********************************************************************************************
    **  @dev The Craft function is inherited from the rarity_crafting contract. The idea is to
    **  provide a way to craft items without having to handle the approve parts. This contract will
    **  do a few manipulations to achieve this.
    **	@param _adventurer: TokenID of the adventurer to craft with
    **	@param _base_type: Category of the item to craft
    **	@param _item_type: Information about the item to craft
    **	@param _crafting_materials: Amount of crafting materials to use
    **********************************************************************************************/
    function craft(uint _adventurer, uint8 _base_type, uint8 _item_type, uint _crafting_materials) external {
        (bool simulation,,,) = _rarityCrafting.simulate(_adventurer, _base_type, _item_type, _crafting_materials);
        require(simulation, "Simulation failed");
        require(_isApprovedOrOwner(_adventurer), "!owner");

        // Allow this contract to craft for the adventurer
        _isApprovedOrApprove(_adventurer, address(this));

        // Contract is doing the needed approves - Note: we could use the actual requirements
        _rarityGold.approve(_adventurer, RARITY_CRAFTING_SUMMMONER_ID, type(uint256).max);
        if (_crafting_materials > 0) {
            _rarityCraftingMaterials.approve(_adventurer, RARITY_CRAFTING_SUMMMONER_ID, type(uint256).max);
        }

        // If the craft succeeds, the NFT crafted should be the current `next_item`
        uint256 nextItem = _rarityCrafting.next_item();

        // As it's synchronous, we register that for this specific item, we expect _adventurer to be the owner
        expected[nextItem] = _adventurer;
        
        // We try to craft. On success, jump to `onERC721Received`
        _rarityCrafting.craft(_adventurer, _base_type, _item_type, _crafting_materials);
        expected[nextItem] = 0;

        // We can now check if the new current `next_item` is not the same as we expected.
        // If so, craft was successful and we can send the NFT to the actual owner
        uint256 newNextItem = _rarityCrafting.next_item();
        if (nextItem != newNextItem) {
            _rarityCrafting.transferFrom(address(this), msg.sender, nextItem);
        }
    }

    /**********************************************************************************************
    **  @dev The contract will receive the NFT from the rarity_crafting contract. Therefor, we need
    **  this function for the SafeMint to be successful. Moreover, because of the missing check on
    **  isApprovedForAll, there is a manipulation to allow the spending of the xp. Little hack.
    **	@param tokenId: ID of the ERC721 being received
    **********************************************************************************************/
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external override returns (bytes4) {
        data; //silence
        require(msg.sender == address(_rarityCrafting), "!rarity_crafting");
        require(operator == address(this), "!operator");
        require(from == address(0), "!mint");
        _rm.approve(address(_rarityCrafting), expected[tokenId]);
        return this.onERC721Received.selector;
    }

    /**********************************************************************************************
    **  @dev Some helper function to retrieve, for a given addresses, all the ERC20 tokens
    **  availables with some relevant information.
    **	@param _owner: address of the owner
    **********************************************************************************************/
    function getItemsByAddress(address _owner) public view returns (Item[] memory) {
        require(_owner != address(0), "cannot retrieve zero address");
        uint256 arrayLength = _rarityCrafting.balanceOf(_owner);

        Item[] memory _items = new Item[](arrayLength);
        for (uint256 i = 0; i < arrayLength; i++) {
            uint256 tokenId = _rarityCrafting.tokenOfOwnerByIndex(_owner, i);
            (uint8 base_type, uint8 item_type,, uint256 crafter) = _rarityCrafting.items(tokenId);
            _items[i] = Item(base_type, item_type, crafter, tokenId);
        }
        return _items;
    }

    /**********************************************************************************************
    **  @dev Check if the msg.sender has the autorization to act on this adventurer
    **	@param _adventurer: TokenID of the adventurer we want to check
    **********************************************************************************************/
    function _isApprovedOrOwner(uint _summoner) internal view returns (bool) {
        return (
            _rm.getApproved(_summoner) == msg.sender ||
            _rm.ownerOf(_summoner) == msg.sender ||
            _rm.isApprovedForAll(_rm.ownerOf(_summoner), msg.sender)
        );
    }

    /**********************************************************************************************
    **  @dev Check if the summoner is approved for this contract as getApprovedForAll is
    **  not used for gold & cellar.
    **	@param _adventurer: TokenID of the adventurer we want to check
    **********************************************************************************************/
    function _isApprovedOrApprove(uint _adventurer, address _operator) internal {
        address _approved = _rm.getApproved(_adventurer);
        if (_approved != _operator) {
            _rm.approve(_operator, _adventurer);
        }
    }
}
