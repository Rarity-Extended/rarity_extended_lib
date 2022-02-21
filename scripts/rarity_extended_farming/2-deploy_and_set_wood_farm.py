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

RARITY_FARMING_CORE_ADDR = "0xEDb761eDE0Fc6f722cb544a6148BE4ccFd6D3a88"
RARITY_FARMING_CORE = rarity_extended_farming_core.at(RARITY_FARMING_CORE_ADDR)

def main():
	# Step 1 - Deploying the Loots contract
	WOOD_LOOT_0 = Contract.from_explorer(RARITY_EXTENDED_WOOD_LOOT_ADDR)
	WOOD_LOOT_1 = Loot.deploy("Soft Wood", "Soft Wood - (Loot)", {"from": DEPLOYER})
	WOOD_LOOT_2 = Loot.deploy("Fine Wood", "Fine Wood - (Loot)", {"from": DEPLOYER})
	WOOD_LOOT_3 = Loot.deploy("Seasoned Wood", "Seasoned Wood - (Loot)", {"from": DEPLOYER})
	WOOD_LOOT_4 = Loot.deploy("Hard Wood", "Hard Wood - (Loot)", {"from": DEPLOYER})
	WOOD_LOOT_5 = Loot.deploy("Darkwood", "Darkwood - (Loot)", {"from": DEPLOYER})

	# Step 2 - Deploying the initial set of farming
	WOOD_FARMING_0 = rarity_extended_farming_base_premium.deploy(
		RARITY_EXTENDED_MS, 5e18,
		RARITY_FARMING_CORE, WOOD_LOOT_0, 1, 0, "Rarity Wood",
		[], [],
		{"from": DEPLOYER}
	)
	WOOD_FARMING_1 = rarity_extended_farming_base_premium.deploy(
		RARITY_EXTENDED_MS, 7e18,
		RARITY_FARMING_CORE, WOOD_LOOT_1, 1, 1, "Rarity Soft Wood", [WOOD_LOOT_0], [12],
		{"from": DEPLOYER}
	)
	WOOD_FARMING_2 = rarity_extended_farming_base_premium.deploy(
		RARITY_EXTENDED_MS, 11e18,
		RARITY_FARMING_CORE, WOOD_LOOT_2, 1, 2, "Rarity Fine Wood",
		[WOOD_LOOT_0, WOOD_LOOT_1], [6, 36],
		{"from": DEPLOYER}
	)
	WOOD_FARMING_3 = rarity_extended_farming_base_premium.deploy(
		RARITY_EXTENDED_MS, 17e18,
		RARITY_FARMING_CORE, WOOD_LOOT_3, 1, 3, "Rarity Seasoned Wood",
		[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2], [6, 18, 72],
		{"from": DEPLOYER}
	)
	
	WOOD_FARMING_4 = rarity_extended_farming_base_premium.deploy(
		RARITY_EXTENDED_MS, 25e18,
		RARITY_FARMING_CORE, WOOD_LOOT_4, 1, 4, "Rarity Hard Wood",
		[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3], [6, 18, 36, 120],
		{"from": DEPLOYER}
	)
	WOOD_FARMING_5 = rarity_extended_farming_base_premium.deploy(
		RARITY_EXTENDED_MS, 35e18,
		RARITY_FARMING_CORE, WOOD_LOOT_5, 1, 5, "Rarity Darkwood",
		[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4], [6, 18, 36, 60, 180],
		{"from": DEPLOYER}
	)
	
	WOOD_FARMING_0 = rarity_extended_farming_base_premium.at('0x10C54867d3513F1326e142a0b1763521FD1cF165')
	WOOD_FARMING_1 = rarity_extended_farming_base_premium.at('0x4fda0067d6111a1D48c9a8BAA933D9e6e0AdC8fD')
	WOOD_FARMING_2 = rarity_extended_farming_base_premium.at('0x6113ca060c6510A3bA82A00A51fE7d0eF194a155')
	WOOD_FARMING_3 = rarity_extended_farming_base_premium.at('0xC1B4C7fd86b8Eeb0dfE94C6b96F5E5F52A5B02a5')
	WOOD_FARMING_4 = rarity_extended_farming_base_premium.at('0x0D27CE28e4D3eF2FcCcf25695800E314726cEB38')
	WOOD_FARMING_5 = rarity_extended_farming_base_premium.at('0xB0986557254055aeC98a2c3d6905C351E0BF61bD')

	# Step 3 - Allowing the farm to mint the loot
	# WOOD_LOOT_0.setMinter(WOOD_FARMING_0, {"from": RARITY_EXTENDED_OP_MS}) //SKIP, TO DO MANUALY
	WOOD_LOOT_1.setMinter(WOOD_FARMING_1, {"from": DEPLOYER})
	WOOD_LOOT_2.setMinter(WOOD_FARMING_2, {"from": DEPLOYER})
	WOOD_LOOT_3.setMinter(WOOD_FARMING_3, {"from": DEPLOYER})
	WOOD_LOOT_4.setMinter(WOOD_FARMING_4, {"from": DEPLOYER})
	WOOD_LOOT_5.setMinter(WOOD_FARMING_5, {"from": DEPLOYER})

	# Step 4 - Linking the slots in the core contract
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_0, {"from": DEPLOYER});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_1, {"from": DEPLOYER});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_2, {"from": DEPLOYER});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_3, {"from": DEPLOYER});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_4, {"from": DEPLOYER});
	RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_5, {"from": DEPLOYER});

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
