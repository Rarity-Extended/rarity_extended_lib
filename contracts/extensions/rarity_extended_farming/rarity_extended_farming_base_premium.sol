// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./rarity_extended_farming_base.sol";

contract rarity_extended_farming_base_premium is rarity_extended_farming_base {
    uint256 immutable BASE_UPGRADE_PRICE;
    address immutable REWARD_ADDRESS;

    /*******************************************************************************
    **  @dev Register the farming contract.
    **	@param _rewardAddress: The address that collects upgrade fees for this farm
    **	@param _upgradePrice: Base upgrade cost for this farm (in FTM)
    **	@param _farmingCore: Core farming contract
    **	@param _farmLoot: Loot item farmed by this contract
    **	@param _farmingType: Can be one of theses, but some more may be added
    **	- 1 for wood
    **	- 2 for minerals
    **	@param _requiredLevel: Level required to access this farm
    **	@param _name: Name of this contract
    **	@param _requiredItems: List of loot items required to unlock this farm
    **	@param _requiredItemsCount: Amount of loots required to unlock this farm
    *******************************************************************************/
	constructor(
        address _rewardAddress,
        uint256 _upgradePrice,
        address _farmingCore,
        address _farmLoot,
        uint8 _farmingType,
        uint _requiredLevel,
        string memory _name,
        address[] memory _requiredItems,
        uint[] memory _requiredItemsCount
    ) rarity_extended_farming_base(_farmingCore, _farmLoot, _farmingType, _requiredLevel, _name, _requiredItems, _requiredItemsCount) {
        REWARD_ADDRESS = _rewardAddress;
        BASE_UPGRADE_PRICE = _upgradePrice;
    }

    /*******************************************************************************
    **  @dev Allow an adventurer to unlock the farm if the requirement are met.
    **	@param _adventurer: adventurer we would like to use with this farm
    **	@param _toUpgradeLevel: level to upgrade to
    *******************************************************************************/
	function _beforeUpgrade(uint _adventurer, uint _toUpgradeLevel) internal override {
        uint256 priceToUpgrade = ((_toUpgradeLevel ** 2) * 1e18) - (_toUpgradeLevel * 1e18) + BASE_UPGRADE_PRICE;
        require(msg.value == priceToUpgrade, "!price");
        payable(REWARD_ADDRESS).transfer(priceToUpgrade);
        _adventurer; //silence!
	}

    /*******************************************************************************
    **  @dev Retrieve the price for an upgrade
    **	@param _toUpgradeLevel: level to upgrade to
    *******************************************************************************/
	function upgradePrice(uint _toUpgradeLevel) public view returns (uint256) {
        return ((_toUpgradeLevel ** 2) * 1e18) - (_toUpgradeLevel * 1e18) + BASE_UPGRADE_PRICE;
	}
}


