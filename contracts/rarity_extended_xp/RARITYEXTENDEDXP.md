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

**[Deployed here](https://ftmscan.com/address/0x640bdeff13ae5527424acd868F65357270b05eB8)**