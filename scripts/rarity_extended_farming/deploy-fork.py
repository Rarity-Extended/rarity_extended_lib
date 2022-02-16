from colorama import Fore, Style
from brownie import (
	accounts, Contract, chain, convert,
	rarity_extended_farming_core,
	rarity_extended_farming_base_premium,
	Loot
)
deployer = accounts[0] # or accounts.load('rarityextended')
rewards = accounts[4]

# Some of the address for Rarity
RARITY_MANIFEST_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
RARITY_EXTENDED_WOOD_LOOT_ADDR = "0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1"
RARITY_EXTENDED_WOOD_LOOT_MINTER_ADDR = "0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3"

# Deploying the Equipement system
RARITY_FARMING_CORE = deployer.deploy(rarity_extended_farming_core)
RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR)

# Deploying the Loots address
WOOD_LOOT_0 = Contract.from_explorer(RARITY_EXTENDED_WOOD_LOOT_ADDR)
WOOD_LOOT_1 = deployer.deploy(Loot, "Soft Wood", "Soft Wood - (Loot)")
WOOD_LOOT_2 = deployer.deploy(Loot, "Fine Wood", "Fine Wood - (Loot)")
WOOD_LOOT_3 = deployer.deploy(Loot, "Seasoned Wood", "Seasoned Wood - (Loot)")
WOOD_LOOT_4 = deployer.deploy(Loot, "Hard Wood", "Hard Wood - (Loot)")
WOOD_LOOT_5 = deployer.deploy(Loot, "Elder Wood", "Elder Wood - (Loot)")

# Deploying the initial set of farming
WOOD_FARMING_0 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 5e18,
	RARITY_FARMING_CORE, WOOD_LOOT_0, 1, 0, "Rarity Wood",
	[], []
)
WOOD_FARMING_1 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 7e18,
	RARITY_FARMING_CORE, WOOD_LOOT_1, 1, 1, "Rarity Soft Wood", [WOOD_LOOT_0], [12]
)
WOOD_FARMING_2 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 11e18,
	RARITY_FARMING_CORE, WOOD_LOOT_2, 1, 2, "Rarity Fine Wood",
	[WOOD_LOOT_0, WOOD_LOOT_1], [6, 36]
)
WOOD_FARMING_3 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 17e18,
	RARITY_FARMING_CORE, WOOD_LOOT_3, 1, 3, "Rarity Seasoned Wood",
	[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2], [6, 18, 72]
)
WOOD_FARMING_4 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 25e18,
	RARITY_FARMING_CORE, WOOD_LOOT_4, 1, 4, "Rarity Hard Wood",
	[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3], [6, 18, 36, 120]
)
WOOD_FARMING_5 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 35e18,
	RARITY_FARMING_CORE, WOOD_LOOT_5, 1, 5, "Rarity Elder Wood",
	[WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4], [6, 18, 36, 60, 180]
)

# Set the farming as loot minters
WOOD_LOOT_0.setMinter(WOOD_FARMING_0, {"from": RARITY_EXTENDED_WOOD_LOOT_MINTER_ADDR})
WOOD_LOOT_1.setMinter(WOOD_FARMING_1, {"from": deployer})
WOOD_LOOT_2.setMinter(WOOD_FARMING_2, {"from": deployer})
WOOD_LOOT_3.setMinter(WOOD_FARMING_3, {"from": deployer})
WOOD_LOOT_4.setMinter(WOOD_FARMING_4, {"from": deployer})
WOOD_LOOT_5.setMinter(WOOD_FARMING_5, {"from": deployer})

# Linking the slots, the wrapped and the contracts
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_0);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_1);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_2);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_3);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_4);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_5);


# Deploying the Loots address
ORE_LOOT_0 = deployer.deploy(Loot, "Copper Ore", "Copper Ore (Loot)")
ORE_LOOT_1 = deployer.deploy(Loot, "Iron Ore", "Iron Ore - (Loot)")
ORE_LOOT_2 = deployer.deploy(Loot, "Gold Ore", "Gold Ore - (Loot)")
ORE_LOOT_3 = deployer.deploy(Loot, "Platinum Ore", "Platinum Ore - (Loot)")
ORE_LOOT_4 = deployer.deploy(Loot, "Mithril Ore", "Mithril Ore - (Loot)")
ORE_LOOT_5 = deployer.deploy(Loot, "Orichalcum Ore", "Orichalcum Ore - (Loot)")

# Deploying the initial set of farming
ORE_FARMING_0 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 5e18,
	RARITY_FARMING_CORE, ORE_LOOT_0, 1, 0, "Rarity Copper Ore",
	[], []
)
ORE_FARMING_1 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 7e18,
	RARITY_FARMING_CORE, ORE_LOOT_1, 1, 1, "Rarity Iron Ore", [ORE_LOOT_0], [12]
)
ORE_FARMING_2 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 11e18,
	RARITY_FARMING_CORE, ORE_LOOT_2, 1, 2, "Rarity Gold Ore",
	[ORE_LOOT_0, ORE_LOOT_1], [6, 36]
)
ORE_FARMING_3 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 17e18,
	RARITY_FARMING_CORE, ORE_LOOT_3, 1, 3, "Rarity Platinum Ore",
	[ORE_LOOT_0, ORE_LOOT_1, ORE_LOOT_2], [6, 18, 72]
)
ORE_FARMING_4 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 25e18,
	RARITY_FARMING_CORE, ORE_LOOT_4, 1, 4, "Rarity Mithril Ore",
	[ORE_LOOT_0, ORE_LOOT_1, ORE_LOOT_2, ORE_LOOT_3], [6, 18, 36, 120]
)
ORE_FARMING_5 = deployer.deploy(rarity_extended_farming_base_premium,
	rewards, 35e18,
	RARITY_FARMING_CORE, ORE_LOOT_5, 1, 5, "Rarity Orichalcum Ore",
	[ORE_LOOT_0, ORE_LOOT_1, ORE_LOOT_2, ORE_LOOT_3, ORE_LOOT_4], [6, 18, 36, 60, 180]
)

# Set the farming as loot minters
ORE_LOOT_0.setMinter(ORE_FARMING_0, {"from": deployer})
ORE_LOOT_1.setMinter(ORE_FARMING_1, {"from": deployer})
ORE_LOOT_2.setMinter(ORE_FARMING_2, {"from": deployer})
ORE_LOOT_3.setMinter(ORE_FARMING_3, {"from": deployer})
ORE_LOOT_4.setMinter(ORE_FARMING_4, {"from": deployer})
ORE_LOOT_5.setMinter(ORE_FARMING_5, {"from": deployer})

# Linking the slots, the wrapped and the contracts
RARITY_FARMING_CORE.registerFarm(ORE_FARMING_0);
RARITY_FARMING_CORE.registerFarm(ORE_FARMING_1);
RARITY_FARMING_CORE.registerFarm(ORE_FARMING_2);
RARITY_FARMING_CORE.registerFarm(ORE_FARMING_3);
RARITY_FARMING_CORE.registerFarm(ORE_FARMING_4);
RARITY_FARMING_CORE.registerFarm(ORE_FARMING_5);

def main():
	print("=================================================================================")
	print("RARITY_EXTENDED_WOOD_LOOT_0: '" + Fore.GREEN + WOOD_LOOT_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_1: '" + Fore.GREEN + WOOD_LOOT_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_2: '" + Fore.GREEN + WOOD_LOOT_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_3: '" + Fore.GREEN + WOOD_LOOT_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_4: '" + Fore.GREEN + WOOD_LOOT_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_5: '" + Fore.GREEN + WOOD_LOOT_5.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_FARM_CORE:   '" + Fore.GREEN + RARITY_FARMING_CORE.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_0: '" + Fore.GREEN + WOOD_FARMING_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_1: '" + Fore.GREEN + WOOD_FARMING_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_2: '" + Fore.GREEN + WOOD_FARMING_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_3: '" + Fore.GREEN + WOOD_FARMING_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_4: '" + Fore.GREEN + WOOD_FARMING_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_5: '" + Fore.GREEN + WOOD_FARMING_5.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_0: '" + Fore.GREEN + ORE_FARMING_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_1: '" + Fore.GREEN + ORE_FARMING_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_2: '" + Fore.GREEN + ORE_FARMING_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_3: '" + Fore.GREEN + ORE_FARMING_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_4: '" + Fore.GREEN + ORE_FARMING_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_ORE_FARM_5: '" + Fore.GREEN + ORE_FARMING_5.address + Style.RESET_ALL + "',")
	print("=================================================================================")
