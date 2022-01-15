## Rarity Extended Lib

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
    ├── test_rarity_extended_xxx.js         # Script to test our xxx library element
    └── test_rarity_extended_yyy.js         # Script to test our yyy library element
```