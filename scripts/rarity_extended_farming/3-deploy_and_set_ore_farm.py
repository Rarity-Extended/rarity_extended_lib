from colorama import Fore, Style
from brownie import (
	accounts, Contract, chain, convert,
	rarity_extended_farming_core,
	rarity_extended_farming_base_premium,
	Loot
)
deployer = accounts.load('rarityextended')

# Some of the address for Rarity
RARITY_EXTENDED_MS = '0x0f5861aaf5F010202919C9126149c6B0c76Cf469'
RARITY_EXTENDED_OP_MS = '0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3'
RARITY_EXTENDED_WOOD_LOOT_ADDR = "0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1"

RARITY_FARMING_CORE_ADDR = ""
RARITY_FARMING_CORE = rarity_extended_farming_core.at(RARITY_FARMING_CORE_ADDR)

def main():
	# Step 1 - Deploying the Loots contract
	ORE_LOOT_0 = deployer.deploy(Loot, "Copper Ore", "Copper Ore (Loot)", publish_source=True, gas_price='250 gwei')
	ORE_LOOT_1 = deployer.deploy(Loot, "Iron Ore", "Iron Ore - (Loot)", publish_source=True, gas_price='250 gwei')
	ORE_LOOT_2 = deployer.deploy(Loot, "Gold Ore", "Gold Ore - (Loot)", publish_source=True, gas_price='250 gwei')
	ORE_LOOT_3 = deployer.deploy(Loot, "Platinum Ore", "Platinum Ore - (Loot)", publish_source=True, gas_price='250 gwei')
	ORE_LOOT_4 = deployer.deploy(Loot, "Mithril Ore", "Mithril Ore - (Loot)", publish_source=True, gas_price='250 gwei')
	ORE_LOOT_5 = deployer.deploy(Loot, "Orichalcum Ore", "Orichalcum Ore - (Loot)", publish_source=True, gas_price='250 gwei')

	# Step 2 - Deploying the initial set of farming
	ORE_FARMING_0 = deployer.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 5e18,
		RARITY_FARMING_CORE, ORE_LOOT_0, 1, 0, "Rarity Copper Ore",
		[], [],
		publish_source=True, gas_price='250 gwei'
	)
	ORE_FARMING_1 = deployer.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 7e18,
		RARITY_FARMING_CORE, ORE_LOOT_1, 1, 1, "Rarity Iron Ore", [ORE_LOOT_0], [12],
		publish_source=True, gas_price='250 gwei'
	)
	ORE_FARMING_2 = deployer.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 11e18,
		RARITY_FARMING_CORE, ORE_LOOT_2, 1, 2, "Rarity Gold Ore",
		[ORE_LOOT_0, ORE_LOOT_1], [6, 36],
		publish_source=True, gas_price='250 gwei'
	)
	ORE_FARMING_3 = deployer.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 17e18,
		RARITY_FARMING_CORE, ORE_LOOT_3, 1, 3, "Rarity Platinum Ore",
		[ORE_LOOT_0, ORE_LOOT_1, ORE_LOOT_2], [6, 18, 72],
		publish_source=True, gas_price='250 gwei'
	)
	ORE_FARMING_4 = deployer.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 25e18,
		RARITY_FARMING_CORE, ORE_LOOT_4, 1, 4, "Rarity Mithril Ore",
		[ORE_LOOT_0, ORE_LOOT_1, ORE_LOOT_2, ORE_LOOT_3], [6, 18, 36, 120],
		publish_source=True, gas_price='250 gwei'
	)
	ORE_FARMING_5 = deployer.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 35e18,
		RARITY_FARMING_CORE, ORE_LOOT_5, 1, 5, "Rarity Orichalcum Ore",
		[ORE_LOOT_0, ORE_LOOT_1, ORE_LOOT_2, ORE_LOOT_3, ORE_LOOT_4], [6, 18, 36, 60, 180],
		publish_source=True, gas_price='250 gwei'
	)

	# Step 3 - Allowing the farm to mint the loot
	ORE_LOOT_0.setMinter(ORE_FARMING_0, {"from": deployer, "gas_price": '250 gwei'})
	ORE_LOOT_1.setMinter(ORE_FARMING_1, {"from": deployer, "gas_price": '250 gwei'})
	ORE_LOOT_2.setMinter(ORE_FARMING_2, {"from": deployer, "gas_price": '250 gwei'})
	ORE_LOOT_3.setMinter(ORE_FARMING_3, {"from": deployer, "gas_price": '250 gwei'})
	ORE_LOOT_4.setMinter(ORE_FARMING_4, {"from": deployer, "gas_price": '250 gwei'})
	ORE_LOOT_5.setMinter(ORE_FARMING_5, {"from": deployer, "gas_price": '250 gwei'})

	# Step 4 - Linking the slots in the core contract
	RARITY_FARMING_CORE.registerFarm(ORE_FARMING_0, {"from": deployer, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(ORE_FARMING_1, {"from": deployer, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(ORE_FARMING_2, {"from": deployer, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(ORE_FARMING_3, {"from": deployer, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(ORE_FARMING_4, {"from": deployer, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(ORE_FARMING_5, {"from": deployer, "gas_price": '250 gwei'});

	print("=================================================================================")
	print("RARITY_EXTENDED_ORE_LOOT_0: '" + Fore.GREEN + ORE_LOOT_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_LOOT_1: '" + Fore.GREEN + ORE_LOOT_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_LOOT_2: '" + Fore.GREEN + ORE_LOOT_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_LOOT_3: '" + Fore.GREEN + ORE_LOOT_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_LOOT_4: '" + Fore.GREEN + ORE_LOOT_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_LOOT_5: '" + Fore.GREEN + ORE_LOOT_5.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_0: '" + Fore.GREEN + ORE_FARMING_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_1: '" + Fore.GREEN + ORE_FARMING_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_2: '" + Fore.GREEN + ORE_FARMING_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_3: '" + Fore.GREEN + ORE_FARMING_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_4: '" + Fore.GREEN + ORE_FARMING_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_5: '" + Fore.GREEN + ORE_FARMING_5.address + Style.RESET_ALL + "',")
	print("=================================================================================")
