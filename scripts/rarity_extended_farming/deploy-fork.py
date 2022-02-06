from curses import wrapper
from brownie import (
	accounts, Contract, convert,
	rarity_extended_farming_wrapper,
	rarity_extended_farming_base,
	Loot
)
deployer = accounts[0] # or accounts.load('rarityextended')

# Some of the address for Rarity
DEVELOPER = ['0x9E63B020ae098E73cF201EE1357EDc72DFEaA518', '636245']
RARITY_MANIFEST_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
RARITY_EXTENDED_WOOD_LOOT_ADDR = "0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1"
RARITY_EXTENDED_WOOD_LOOT_MINTER_ADDR = "0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3"

# Deploying the Equipement system
RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR)
WRAPPER = deployer.deploy(rarity_extended_farming_wrapper)

print("=================================================================================")
print(WRAPPER.xpRequired(1))
print(WRAPPER.xpRequired(2))
print(WRAPPER.xpRequired(3))
print(WRAPPER.xpRequired(4))
print(WRAPPER.xpRequired(5))
print(WRAPPER.xpRequired(6))
print(WRAPPER.xpRequired(7))
print(WRAPPER.xpRequired(8))
print(WRAPPER.xpRequired(9))
print(WRAPPER.xpRequired(10))
print("=================================================================================")


# Deploying the Loots address
WOOD_LOOT_1 = Contract.from_explorer(RARITY_EXTENDED_WOOD_LOOT_ADDR)
WOOD_LOOT_2 = deployer.deploy(Loot, "Soft Wood", "Soft Wood - (Loot)")
WOOD_LOOT_3 = deployer.deploy(Loot, "Seasoned Wood", "Seasoned Wood - (Loot)")
WOOD_LOOT_4 = deployer.deploy(Loot, "Hard Wood", "Hard Wood - (Loot)")
WOOD_LOOT_5 = deployer.deploy(Loot, "Elder Wood", "Elder Wood - (Loot)")
WOOD_LOOT_6 = deployer.deploy(Loot, "Ancient Wood", "Ancient Wood - (Loot)")

# Deploying the initial set of farming
WOOD_FARMING_1 = deployer.deploy(
	rarity_extended_farming_base,
	1,
	10,
	WRAPPER,
	RARITY_EXTENDED_WOOD_LOOT_ADDR,
	"Rarity Extended Farming - Wood",
	0,
	[],
	[]
)
WOOD_FARMING_2 = deployer.deploy(
	rarity_extended_farming_base,
	1,
	8,
	WRAPPER,
	WOOD_LOOT_2.address,
	"Rarity Extended Farming - Soft Wood",
	1750,
	[WOOD_LOOT_1],
	[50]
)
WOOD_FARMING_3 = deployer.deploy(
	rarity_extended_farming_base,
	1,
	6,
	WRAPPER,
	WOOD_LOOT_3.address,
	"Rarity Extended Farming - Seasoned Wood",
	5250,
	[WOOD_LOOT_1, WOOD_LOOT_2],
	[100, 80]
)
WOOD_FARMING_4 = deployer.deploy(
	rarity_extended_farming_base,
	1,
	4,
	WRAPPER,
	WOOD_LOOT_4.address,
	"Rarity Extended Farming - Hard Wood",
	12250,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3],
	[200, 160, 115]
)
WOOD_FARMING_5 = deployer.deploy(
	rarity_extended_farming_base,
	1,
	2,
	WRAPPER,
	WOOD_LOOT_5.address,
	"Rarity Extended Farming - Elder Wood",
	22750,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4],
	[300, 200, 150, 115]
)
WOOD_FARMING_6 = deployer.deploy(
	rarity_extended_farming_base,
	1,
	1,
	WRAPPER,
	WOOD_LOOT_6.address,
	"Rarity Extended Farming - Ancient Wood",
	36750,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4, WOOD_LOOT_5],
	[400, 300, 225, 150, 115]
)

# Set the farming as loot minters
WOOD_LOOT_1.setMinter(WOOD_FARMING_1, {"from": RARITY_EXTENDED_WOOD_LOOT_MINTER_ADDR})
WOOD_LOOT_2.setMinter(WOOD_FARMING_2, {"from": deployer})
WOOD_LOOT_3.setMinter(WOOD_FARMING_3, {"from": deployer})
WOOD_LOOT_4.setMinter(WOOD_FARMING_4, {"from": deployer})
WOOD_LOOT_5.setMinter(WOOD_FARMING_5, {"from": deployer})
WOOD_LOOT_6.setMinter(WOOD_FARMING_6, {"from": deployer})

# Linking the slots, the wrapped and the contracts
WRAPPER.registerFarm(WOOD_FARMING_1);
WRAPPER.registerFarm(WOOD_FARMING_2);
WRAPPER.registerFarm(WOOD_FARMING_3);
WRAPPER.registerFarm(WOOD_FARMING_4);
WRAPPER.registerFarm(WOOD_FARMING_5);
WRAPPER.registerFarm(WOOD_FARMING_6);

def printEnv():
	print("=================================================================================")
	print("RARITY_FARMING_WRAPPER_ADDR: " + WRAPPER.address)
	print("RARITY_FARMING_WOOD_1_ADDR: " + WOOD_FARMING_1.address)
	print("RARITY_FARMING_WOOD_2_ADDR: " + WOOD_FARMING_2.address)
	print("RARITY_FARMING_WOOD_3_ADDR: " + WOOD_FARMING_3.address)
	print("RARITY_FARMING_WOOD_4_ADDR: " + WOOD_FARMING_4.address)
	print("RARITY_FARMING_WOOD_5_ADDR: " + WOOD_FARMING_5.address)
	print("RARITY_FARMING_WOOD_6_ADDR: " + WOOD_FARMING_6.address)
	print("=================================================================================")

def runFarm():
	print("WOOD: " + convert.to_string(WOOD_LOOT_1.balanceOf(DEVELOPER[1])))
	print("SOFT_WOOD: " + convert.to_string(WOOD_LOOT_2.balanceOf(DEVELOPER[1])))
	print("XP: " + convert.to_string(WRAPPER.xp(DEVELOPER[1], 1)))
	
	WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
	# WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
	
	print("WOOD: " + convert.to_string(WOOD_LOOT_1.balanceOf(DEVELOPER[1])))
	print("SOFT_WOOD: " + convert.to_string(WOOD_LOOT_2.balanceOf(DEVELOPER[1])))
	print("XP: " + convert.to_string(WRAPPER.xp(DEVELOPER[1], 1)))


def main():
	printEnv()
	runFarm()
