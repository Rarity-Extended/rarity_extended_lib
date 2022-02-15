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
│   ├── dummies/                            # Dummy versions of different contracts, used for testing only
│   ├── interfaces/                         # All shared interfaces
│   ├── rarity_extended_xxx/                # One of your library element
│   └── rarity_extended_yyy/                # Another library element
├── scripts/
│   ├── _deploy_template.js                 # File to use as template for our deploy scripts
│   ├── deploy_rarity_extended_xxx.js       # Script to deploy our xxx library element
│   └── deploy_rarity_extended_yyy.js       # Script to deploy our yyy library element
├── test/
│    ├── _test_template.js                  # File to use as template for our tests files
│    ├── _test_utils.js                     # Set of functions to use for our tests
│    ├── tests_rarity_extended_xxx.js       # Script to test our xxx library element
└── core/                                   # Core contracts of Rarity Manifested (Work by Andre Cronje)
```

* [Deployed contracts](DEPLOYEDCONTRACTS.md)

* [Rarity Extended Care](contracts/rarity_extended_care/RARITYEXTENDEDCARE.md)
* [Rarity Extended Name](contracts/rarity_extended_name/RARITYEXTENDEDNAME.md)
* [Rarity Extended XP](contracts/rarity_extended_xp/RARITYEXTENDEDXP.md)
* [Rarity Extended Cooking Helper](contracts/rarity_extended_cooking_helper/RARITYEXTENDEDCOOKINGHELPER.md)
* [Rarity Extended Crafting Helper](contracts/rarity_extended_crafting_helper/RARITYEXTENDEDCRAFTINGHELPER.md)
* [Rarity Extended Equipement](contracts/rarity_extended_equipement/RARITYEXTENDEDEQUIPEMENT.md)
* [Rarity Extended Equipement Basic Set](contracts/rarity_extended_equipement_basic_set/RARITYEXTENDEDEQUIPEMENTBASICSET.md)
* [Rarity Extended Farming](contracts/rarity_extended_farming/RARITYEXTENDEDFARMING.md)
* [Rarity Extended Proxy Deployer](contracts/rarity_extended_proxy_deployer/RARITYPROXYDEPLOYER.md)
* [Rarity Extended Skin Helper](contracts/rarity_extended_skin_helper/RARITYEXTENDEDSKINHELPER.md)
* [Rarity Extended Utils](contracts/utils/UTILS.md)
* [Rarity Extended Extra](contracts/RARITYEXTENDEDEXTRA.md)