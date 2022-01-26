# Rarity Extended Lib

Hello to the world of Rarity Extended!  
Here, you will be able to find our most recent additions to the game. Theses additions can take various forms, from new items to new abilities to new enemies, or simply to helpers or facilitators.  
Here is the architecture for the repo: 
```
RarityExtended/
├── README.md
├── package.json                            # The dependencies
├── hardhat.config                          # The default config for hardhat
├── .env                                    # The environment variables
├── contracts/
│   ├── interfaces/                         # All shared interfaces
│   ├── rarity_extended_xxx/                # One of your library element
│   └── rarity_extended_yyy/                # Another library element
├── scripts/
│   ├── _deploy_template.js                 # File to use as template for our deploy scripts
│   ├── deploy_rarity_extended_xxx.js       # Script to deploy our xxx library element
│   └── deploy_rarity_extended_yyy.js       # Script to deploy our yyy library element
└── test/
    ├── _test_template.js                   # File to use as template for our tests files
    ├── _test_utils.js                      # Set of functions to use for our tests
    ├── tests_rarity_extended_xxx.js         # Script to test our xxx library element
    └── tests_rarity_extended_yyy.js         # Script to test our yyy library element
```

## Deployed contracts
> Helpers and facilitators
- [Rarity Extended Name - 0x4762AF980240eFEBbc2D6E46C408A720C20D0e10](https://ftmscan.com/address/0x4762AF980240eFEBbc2D6E46C408A720C20D0e10)
- [Rarity Extended Care - 0xc066618F5c84D2eB002b99b020364D4CDDE6245D](https://ftmscan.com/address/0xc066618F5c84D2eB002b99b020364D4CDDE6245D)
- [Rarity Extended XP - 0x640bdeff13ae5527424acd868F65357270b05eB8](https://ftmscan.com/address/0x640bdeff13ae5527424acd868F65357270b05eB8)
- [Rarity Extended Skins Helper - 0xbe570c81e8bc6a4ca2675fe619044b389df32566](https://ftmscan.com/address/0xbe570c81e8bc6a4ca2675fe619044b389df32566)
- [Rarity Extended Proxy Deployer - 0x253aaEAFDA7AE3C6Ed3E3E2732C49cf077a22Ae0](https://ftmscan.com/address/0x253aaEAFDA7AE3C6Ed3E3E2732C49cf077a22Ae0
- [Rarity Extended Cooking - 0x7474002fe5640d612c9a76cb0b6857932ff891e8](https://ftmscan.com/address/0x7474002fe5640d612c9a76cb0b6857932ff891e8)
- [Rarity Extended Cooking Helper - 0xFE23ea8C57Ee4f28E9C60cA09C512Ce80e90E6F5](https://ftmscan.com/address/0xFE23ea8C57Ee4f28E9C60cA09C512Ce80e90E6F5)

> Loots
- [Rarity Extended rERC20 - Mushroom - 0xcd80cE7E28fC9288e20b806ca53683a439041738](https://ftmscan.com/address/0xcd80cE7E28fC9288e20b806ca53683a439041738)
- [Rarity Extended rERC20 - Berries - 0x9d6C92CCa7d8936ade0976282B82F921F7C50696](https://ftmscan.com/address/0x9d6C92CCa7d8936ade0976282B82F921F7C50696)
- [Rarity Extended rERC20 - Wood - 0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1](https://ftmscan.com/address/0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1)
- [Rarity Extended rERC20 - Leather - 0xc5E80Eef433AF03E9380123C75231A08dC18C4B6](https://ftmscan.com/address/0xc5E80Eef433AF03E9380123C75231A08dC18C4B6)
- [Rarity Extended rERC20 - Meat - 0x95174B2c7E08986eE44D65252E3323A782429809](https://ftmscan.com/address/0x95174B2c7E08986eE44D65252E3323A782429809)
- [Rarity Extended rERC20 - Tusks - 0x60bFaCc2F96f3EE847cA7D8cC713Ee40114be667](https://ftmscan.com/address/0x60bFaCc2F96f3EE847cA7D8cC713Ee40114be667)
- [Rarity Extended rERC20 - Candies - 0x18733f3C91478B122bd0880f41411efd9988D97E](https://ftmscan.com/address/0x18733f3C91478B122bd0880f41411efd9988D97E)

> Meals
- [Rarity Extended rERC721 - Meal Grilled Meat - 0x97e8f1061224cb532f808b074786c76e977ba6ee](https://ftmscan.com/address/0x97e8f1061224cb532f808b074786c76e977ba6ee)
- [Rarity Extended rERC721 - Meal Mushroom soup - 0x2e3e1c1f49a288ebf88be66a3ed3539b5971f25d](https://ftmscan.com/address/0x2e3e1c1f49a288ebf88be66a3ed3539b5971f25d)
- [Rarity Extended rERC721 - Meal Berries pie - 0x57e4cd55289da26aa7cb607c00c5ddcd0f7980a2](https://ftmscan.com/address/0x57e4cd55289da26aa7cb607c00c5ddcd0f7980a2)
- [Rarity Extended rERC721 - Meal Mushroom and Meat Skewer - 0x65567a2fbc14b4abcd414bb6902384745d4353f6](https://ftmscan.com/address/0x65567a2fbc14b4abcd414bb6902384745d4353f6)
- [Rarity Extended rERC721 - Meal Mushroom and Berries Mix - 0xf06ffe67cb96641eec55ea19126bd8f0107ff0ad](https://ftmscan.com/address/0xf06ffe67cb96641eec55ea19126bd8f0107ff0ad)
- [Rarity Extended rERC721 - Meal Berries Wine - 0xa0e9159efc4407c4465bbcdf0e7538d6869d81a3](https://ftmscan.com/address/0xa0e9159efc4407c4465bbcdf0e7538d6869d81a3)


## RarityExtended Care
Rarity Extended Care is a smartContract that will be used with RarityExtended to provide a more advanced and secure way to manage all of your adventurers in one call.  
This can be see as an extension of Rarity to be able to perfom batch actions, including :
- **Performing the daily Adventure**
- **Performing the daily Cellar**
- **Level upping your adventurers**
- **Claiming gold for your adventurers**

All of them can be done individually, but it is recommended to use the batch action, aka `care_of`.


#### Usage
In order to be able to use this contract with your summoners, you must, first, call the `setApprovalForAll` function of the `Rarity` contract.  
Here is the function :  
```js
function setApprovalForAll(address operator, bool approved) public virtual override {
    require(operator != msg.sender, "ERC721: approve to caller");

    _operatorApprovals[msg.sender][operator] = approved;
    emit ApprovalForAll(msg.sender, operator, approved);
}
```

This function is not very safe and must be used with caution : It allows the `Operator` to perform approval in your name for all your summoners. We are using this function to allow the `Extended Care` to perform the daily actions of the `Rarity` contract for you, saving gas and preventing multiple transaction. This contract doesn't have the possibility to move your funds or summoner.

Once you have performed the setApprovalForAll, you can use the `care_of` function to perform the batch actions.
```js
function care_of(uint[] memory _summoners, bool[4] memory _whatToDo, uint _threshold_cellar) external
```

The `care_of` function takes 3 parameters :
- `_summoners` : The array of summoners to perform the batch actions.
- `_whatToDo` : The array of boolean that represent the actions to perform. The order is : `[daily_adventure, daily_cellar, level_up, claim_gold]`.
- `_threshold_cellar` : The threshold to perform the cellar.

For example, if you want to perform the daily adventure + the daily cellar for all your summoners, you can do :
```js
care_of([12345, 23456, 65432], [true, true, false, false], 1)
```

-----------------------

## RarityExtended Name
Rarity Extended Name is a smartContract that will be used with RarityExtended to provide some personalization on the aventurers, allowing the players to set names for their characters, including :
- **The Firstname** aka `John` for example
- **The Lastname** aka `Doe` for example
- **The Surname** aka `The mighty Unknow Warrior` for example

There is no specific restrictions, names can be anything you want, but it's better to keep it short, may or may not be unique. You can use the same name for multiple characters, and UIs can choose to use your full name or some parts.
This is supposed to be an alternative to [Rarity Name](https://ftmscan.com/address/0xc73e1237a5a9ba5b0f790b6580f32d04a727dc19) (which work more like an ENS) to get a bit more "RP feel".

**[Deployed here](https://ftmscan.com/address/0x4762AF980240eFEBbc2D6E46C408A720C20D0e10)**

--------------


## RarityExtended XP
The adventurers, in Rarity, are some ERC721 tokens, aka NFT.  
The standard used for ERC721 has an approve function. This approve function allows one address to perform some specific actions in the name of the NFT owner.  
Unlike ERC20 approvals, this approval does not stack : you can only have 1 approve for 1 address at any given time.  
*What does that mean ?* : I have an adventurer and I want to send him to The Forest. I approve the Forest to use my adventurer. Then I want to craft something. I approve the Blacksmith to use my adventurer. Then I want to send him to the Forest : again I have to **re**approve my adventurer.  
This situation is not ideal.  

But why do we need to approve our adventurers ? Only to spend some XP (crafting can require an amount of XP, same as the Forest (actually no, but for the example)).  
We decided to build a Proxy for XP that could you the same way as ERC20 approvals. Indeed, thanks to the standard `setApprovalForAll` function in ERC721 contract (rarity for example) we can allow a specific address (this contract) to get an approval for every tokens owned by this address, without the approval being deleted if another approve is done. *This can be dangerous, but this contract is restricted to some specific use.*. Then it will just work in the same way as an ERC20 !  

#### How to proceed
1. `rarity.setApprovalForAll(rarityXPProxyAddress, true)` to allow this contract to spend the XP of your adventurers
2. `rarityXPProxy.approve(MY_ADVENTURER_ID, THE_OPERATOR_AKA_THE_CRAFTING_CONTRACT, AMOUNT)` to allow the operator contract (that use rarityXPProxy) to spend some of your XP (AMOUNT xp to be exact, at most)
3. `rarityXPProxy.spendXp(MY_ADVENTURER_ID, AMOUNT)` the operator will be able to spend XP for my adventurer, with this correct allowance

#### Update on RarityCrafting to integrate RarityXPProxy
```diff
contract rarity_crafting is ERC721Enumerable {
    [...]    
+    rarity_xp_proxy constant _xp = rarity_xp_proxy(ADDRESS_OF_THIS_CONTRACT);

    function craft(uint _summoner, uint8 _base_type, uint8 _item_type, uint _crafting_materials) external {
        require(_isApprovedOrOwner(_summoner), "!owner");
        require(_attr.character_created(_summoner), "!created");
        require(_summoner != SUMMMONER_ID, "hax0r");
        require(isValid(_base_type, _item_type), "!valid");
        uint _dc = get_dc(_base_type, _item_type);
        if (_crafting_materials >= 10) {
            require(_craft_i.transferFrom(SUMMMONER_ID, _summoner, SUMMMONER_ID, _crafting_materials), "!craft");
            _dc = _dc - (_crafting_materials / 10);
        }
        (bool crafted, int check) = craft_skillcheck(_summoner, _dc);
        if (crafted) {
            uint _cost = get_item_cost(_base_type, _item_type);
            require(_gold.transferFrom(SUMMMONER_ID, _summoner, SUMMMONER_ID, _cost), "!gold");
            items[next_item] = item(_base_type, _item_type, uint32(block.timestamp), _summoner);
            _safeMint(msg.sender, next_item);
            emit Crafted(msg.sender, uint(check), _summoner, _base_type, _item_type, _cost, _crafting_materials);
            next_item++;
        }
-        _rm.spend_xp(_summoner, craft_xp_per_day);
+        _xp.spend_xp(_summoner, craft_xp_per_day);
    }
```

----------------------

## RarityExtended ERC20
Variant of the ERC20 standard used for the Rarity specific adventurer system.
Used by Rarity Extended.

*Original work by TheAustrian for the Boars Adventure.*

------

## RarityExtended Proxy Deployer

A proxy contract to deploy others contract, passing the bytecode in parameters, used for deploy contracts with a Gnosis Safe Multisig