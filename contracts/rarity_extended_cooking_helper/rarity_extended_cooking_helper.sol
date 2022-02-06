// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "../interfaces/IRarity.sol";
import "../interfaces/IrERC20.sol";
import "../interfaces/IRarityCooking.sol";

contract rarity_extended_cooking_helper {
    string constant public name = "Rarity Extended Cooking Helper";

    // Define the list of addresse we will need to interact with
    IRarity constant _rm = IRarity(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    IrERC20 constant _rarityGold = IrERC20(0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2);
    IRarityCooking immutable _rarityCooking;
    uint immutable RARITY_COOKING_SUMMMONER_ID; //NPC of the RarityCooking contract

    constructor(address _rarityCookingAddress) {
        _rarityCooking = IRarityCooking(_rarityCookingAddress);
        RARITY_COOKING_SUMMMONER_ID = _rarityCooking.summonerCook();
    }

    /**********************************************************************************************
    **  @dev The Craft function is inherited from the rarity_crafting contract. The idea is to
    **  provide a way to craft items without having to handle the approve parts. This contract will
    **  do a few manipulations to achieve this.
    **	@param _adventurer: TokenID of the adventurer to craft with
    **	@param _base_type: Category of the item to craft
    **	@param _item_type: Information about the item to craft
    **	@param _crafting_materials: Amount of crafting materials to use
    **********************************************************************************************/
    function cook(address _meal, uint _adventurer, uint _receiver) external {
        require(_isApprovedOrOwner(_adventurer), "!owner");

        // Allow this contract to craft for the adventurer
        _isApprovedOrApprove(_adventurer, address(this));

        (,,address[] memory ingredients, uint[] memory quantities) = _rarityCooking.getRecipe(_meal);

        for (uint i = 0; i < ingredients.length; i++) {
            IrERC20(ingredients[i]).approve(_adventurer, RARITY_COOKING_SUMMMONER_ID, quantities[i]);
        }
        
        _rarityCooking.cook(_meal, _adventurer, _receiver);
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
