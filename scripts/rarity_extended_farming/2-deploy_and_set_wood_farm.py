from colorama import Fore, Style
from brownie import (
	accounts, Contract,
	rarity_extended_farming_core,
	rarity_extended_farming_base_premium,
	Loot
)
DEPLOYER = accounts.load('rarityextended')

# Some of the address for Rarity
RARITY_EXTENDED_MS = '0x0f5861aaf5F010202919C9126149c6B0c76Cf469'
RARITY_EXTENDED_OP_MS = '0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3'
RARITY_EXTENDED_WOOD_LOOT_ADDR = "0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1"

RARITY_FARMING_CORE_ADDR = ""
RARITY_FARMING_CORE = rarity_extended_farming_core.at(RARITY_FARMING_CORE_ADDR)

def main():
	# Step 1 - Deploying the Loots contract
	WOOD_LOOT_0 = Contract.from_explorer(RARITY_EXTENDED_WOOD_LOOT_ADDR)
	WOOD_LOOT_1 = DEPLOYER.deploy(Loot, "Soft Wood", "Soft Wood - (Loot)", publish_source=True, gas_price='250 gwei')
	WOOD_LOOT_2 = DEPLOYER.deploy(Loot, "Fine Wood", "Fine Wood - (Loot)", publish_source=True, gas_price='250 gwei')
	WOOD_LOOT_3 = DEPLOYER.deploy(Loot, "Seasoned Wood", "Seasoned Wood - (Loot)", publish_source=True, gas_price='250 gwei')
	WOOD_LOOT_4 = DEPLOYER.deploy(Loot, "Hard Wood", "Hard Wood - (Loot)", publish_source=True, gas_price='250 gwei')
	WOOD_LOOT_5 = DEPLOYER.deploy(Loot, "Darkwood", "Darkwood - (Loot)", publish_source=True, gas_price='250 gwei')

	# Step 2 - Deploying the initial set of farming
	WOOD_FARMING_0 = DEPLOYER.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 5e18,
		RARITY_FARMING_CORE, WOOD_LOOT_0, 1, 0, "Rarity Wood",
		[], [],
		publish_source=True, gas_price='250 gwei'
	)
	WOOD_FARMING_1 = DEPLOYER.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 7e18,
		RARITY_FARMING_CORE, WOOD_LOOT_1, 1, 1, "Rarity Soft Wood", [WOOD_LOOT_0], [12],
		publish_source=True, gas_price='250 gwei'
	)
	WOOD_FARMING_2 = DEPLOYER.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 11e18,
		RARITY_FARMING_CORE, WOOD_LOOT_2, 1, 2, "Rarity Fine Wood",
		[WOOD_LOOT_0, WOOD_LOOT_1], [6, 36],
		publish_source=True, gas_price='250 gwei'
	)
	WOOD_FARMING_3 = DEPLOYER.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 17e18,
		RARITY_FARMING_CORE, WOOD_LOOT_3, 1, 3, "Rarity Seasoned Wood",
		[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2], [6, 18, 72],
		publish_source=True, gas_price='250 gwei'
	)
	WOOD_FARMING_4 = DEPLOYER.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 25e18,
		RARITY_FARMING_CORE, WOOD_LOOT_4, 1, 4, "Rarity Hard Wood",
		[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3], [6, 18, 36, 120],
		publish_source=True, gas_price='250 gwei'
	)
	WOOD_FARMING_5 = DEPLOYER.deploy(rarity_extended_farming_base_premium,
		RARITY_EXTENDED_MS, 35e18,
		RARITY_FARMING_CORE, WOOD_LOOT_5, 1, 5, "Rarity Darkwood",
		[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4], [6, 18, 36, 60, 180],
		publish_source=True, gas_price='250 gwei'
	)

	# Step 3 - Allowing the farm to mint the loot
	# WOOD_LOOT_0.setMinter(WOOD_FARMING_0, {"from": RARITY_EXTENDED_OP_MS}) //SKIP, TO DO MANUALY
	WOOD_LOOT_1.setMinter(WOOD_FARMING_1, {"from": DEPLOYER, "gas_price": '250 gwei'})
	WOOD_LOOT_2.setMinter(WOOD_FARMING_2, {"from": DEPLOYER, "gas_price": '250 gwei'})
	WOOD_LOOT_3.setMinter(WOOD_FARMING_3, {"from": DEPLOYER, "gas_price": '250 gwei'})
	WOOD_LOOT_4.setMinter(WOOD_FARMING_4, {"from": DEPLOYER, "gas_price": '250 gwei'})
	WOOD_LOOT_5.setMinter(WOOD_FARMING_5, {"from": DEPLOYER, "gas_price": '250 gwei'})

	# Step 4 - Linking the slots in the core contract
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_0, {"from": DEPLOYER, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_1, {"from": DEPLOYER, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_2, {"from": DEPLOYER, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_3, {"from": DEPLOYER, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_4, {"from": DEPLOYER, "gas_price": '250 gwei'});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_5, {"from": DEPLOYER, "gas_price": '250 gwei'});

	print("=================================================================================")
	print("RARITY_EXTENDED_WOOD_LOOT_0: '" + Fore.GREEN + WOOD_LOOT_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_1: '" + Fore.GREEN + WOOD_LOOT_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_2: '" + Fore.GREEN + WOOD_LOOT_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_3: '" + Fore.GREEN + WOOD_LOOT_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_4: '" + Fore.GREEN + WOOD_LOOT_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_5: '" + Fore.GREEN + WOOD_LOOT_5.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_0: '" + Fore.GREEN + WOOD_FARMING_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_1: '" + Fore.GREEN + WOOD_FARMING_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_2: '" + Fore.GREEN + WOOD_FARMING_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_3: '" + Fore.GREEN + WOOD_FARMING_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_4: '" + Fore.GREEN + WOOD_FARMING_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_5: '" + Fore.GREEN + WOOD_FARMING_5.address + Style.RESET_ALL + "',")
	print("=================================================================================")
	print(DEPLOYER.balance().to('ether'))
