from colorama import Fore, Back, Style
from brownie import (
	accounts, Contract, chain, convert,
	rarity_extended_farming_core,
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
RARITY_FARMING_CORE = deployer.deploy(rarity_extended_farming_core)
RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR)

# Deploying the Loots address
WOOD_LOOT_0 = Contract.from_explorer(RARITY_EXTENDED_WOOD_LOOT_ADDR)
WOOD_LOOT_1 = deployer.deploy(Loot, "Soft Wood", "Soft Wood - (Loot)")
WOOD_LOOT_2 = deployer.deploy(Loot, "Fine Wood", "Fine Wood - (Loot)")
WOOD_LOOT_3 = deployer.deploy(Loot, "Seasoned Wood", "Seasoned Wood - (Loot)")
WOOD_LOOT_4 = deployer.deploy(Loot, "Hard Wood", "Hard Wood - (Loot)")
WOOD_LOOT_5 = deployer.deploy(Loot, "Elder Wood", "Elder Wood - (Loot)")
WOOD_LOOT_6 = deployer.deploy(Loot, "Ancient Wood", "Ancient Wood - (Loot)")


# Deploying the initial set of farming
WOOD_FARMING_0 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_0.address, "Rarity Wood",
	0, [], []
)
WOOD_FARMING_1 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_1.address, "Rarity Soft Wood",
	1, [WOOD_LOOT_0], [12]
)
WOOD_FARMING_2 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_2.address, "Rarity Fine Wood",
	2, [WOOD_LOOT_0, WOOD_LOOT_1], [6, 36]
)
WOOD_FARMING_3 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_3.address, "Rarity Seasoned Wood",
	3, [WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2], [6, 18, 72]
)
WOOD_FARMING_4 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_4.address, "Rarity Hard Wood",
	4, [WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3], [6, 18, 36, 120]
)
WOOD_FARMING_5 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_5.address, "Rarity Elder Wood",
	5, [WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4], [6, 18, 36, 60, 180]
)
WOOD_FARMING_6 = deployer.deploy(rarity_extended_farming_base, 1, RARITY_FARMING_CORE, WOOD_LOOT_6.address, "Rarity Ancient Wood",
	6, [WOOD_LOOT_0, WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4, WOOD_LOOT_5], [6, 18, 36, 60, 90, 252]
)

# Set the farming as loot minters
WOOD_LOOT_0.setMinter(WOOD_FARMING_0, {"from": RARITY_EXTENDED_WOOD_LOOT_MINTER_ADDR})
WOOD_LOOT_1.setMinter(WOOD_FARMING_1, {"from": deployer})
WOOD_LOOT_2.setMinter(WOOD_FARMING_2, {"from": deployer})
WOOD_LOOT_3.setMinter(WOOD_FARMING_3, {"from": deployer})
WOOD_LOOT_4.setMinter(WOOD_FARMING_4, {"from": deployer})
WOOD_LOOT_5.setMinter(WOOD_FARMING_5, {"from": deployer})
WOOD_LOOT_6.setMinter(WOOD_FARMING_6, {"from": deployer})

# Linking the slots, the wrapped and the contracts
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_0);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_1);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_2);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_3);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_4);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_5);
RARITY_FARMING_CORE.registerFarm(WOOD_FARMING_6);

days = 0
previousWoodT0 = 0
previousWoodT1 = 0
previousWoodT2 = 0
previousWoodT3 = 0
previousWoodT4 = 0
previousWoodT5 = 0

def printStatus():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4, previousWoodT5

	_totalWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	_earnedWoodT0 = _totalWoodT0 - previousWoodT0
	previousWoodT0 = _totalWoodT0

	_totalWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	_earnedWoodT1 = _totalWoodT1 - previousWoodT2
	previousWoodT1 = _totalWoodT1

	_totalWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	_earnedWoodT2 = _totalWoodT2 - previousWoodT2
	previousWoodT2 = _totalWoodT2

	_totalWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	_earnedWoodT3 = _totalWoodT3 - previousWoodT3
	previousWoodT3 = _totalWoodT3

	_totalWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	_earnedWoodT4 = _totalWoodT4 - previousWoodT4
	previousWoodT4 = _totalWoodT4

	_totalWoodT5 = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);
	_earnedWoodT5 = _totalWoodT5 - previousWoodT5
	previousWoodT5 = _totalWoodT5

	print("\n=================================================================================")
	print("WOOD T0: " + convert.to_string(_totalWoodT0), end="")
	if (_earnedWoodT0 > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWoodT0) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("WOOD T1: " + convert.to_string(_totalWoodT1), end="")
	if (_earnedWoodT1 > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWoodT1) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("WOOD T2: " + convert.to_string(_totalWoodT2), end="")
	if (_earnedWoodT2 > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWoodT2) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("WOOD T3: " + convert.to_string(_totalWoodT3), end="")
	if (_earnedWoodT3 > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWoodT3) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("WOOD T4: " + convert.to_string(_totalWoodT4), end="")
	if (_earnedWoodT4 > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWoodT4) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("WOOD T5: " + convert.to_string(_totalWoodT5), end="")
	if (_earnedWoodT5 > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWoodT5) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("XP: " + convert.to_string(RARITY_FARMING_CORE.xp(DEVELOPER[1], 1)))
	print("DAYS: " + convert.to_string(days))
	print("=================================================================================")

def runFarmFrom0To1():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4

	while True:
		WOOD_FARMING_0.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})

		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1

		if (RARITY_FARMING_CORE.xp(DEVELOPER[1], 1) >= RARITY_FARMING_CORE.xpRequired(1)):
			RARITY_FARMING_CORE.levelup(DEVELOPER[1], 1, {"from": DEVELOPER[0]})
			print("\n" + Fore.GREEN + 'Level up!' + Style.RESET_ALL)

		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) >= 12) and (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) == 1):
			break
	
	WOOD_LOOT_0.approve(DEVELOPER[1], WOOD_FARMING_1.RARITY_EXTENDED_NCP(), 12, {"from": DEVELOPER[0]})
	WOOD_FARMING_1.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n", Fore.GREEN + 'Tier 1 unlocked!' + Style.RESET_ALL)
	previousWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	previousWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	previousWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);

def runFarmFrom1To2():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4

	while True:
		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) < 6):
			WOOD_FARMING_0.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})

		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1

		if (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) < 2) and (RARITY_FARMING_CORE.xp(DEVELOPER[1], 1) >= RARITY_FARMING_CORE.xpRequired(2)):
			RARITY_FARMING_CORE.levelup(DEVELOPER[1], 1, {"from": DEVELOPER[0]})
			print("\n" + Fore.GREEN + 'Level up!' + Style.RESET_ALL)

		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) >= 6) and (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 36) and (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) == 2):
			break
	
	WOOD_LOOT_0.approve(DEVELOPER[1], WOOD_FARMING_2.RARITY_EXTENDED_NCP(), 6, {"from": DEVELOPER[0]})
	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_2.RARITY_EXTENDED_NCP(), 36, {"from": DEVELOPER[0]})
	WOOD_FARMING_2.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n", Fore.GREEN + 'Tier 2 unlocked!' + Style.RESET_ALL)
	previousWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	previousWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	previousWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);

def runFarmFrom2To3():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4

	while True:
		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) < 6):
			WOOD_FARMING_0.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) < 18):
			WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})

		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1

		if (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) < 3) and (RARITY_FARMING_CORE.xp(DEVELOPER[1], 1) >= RARITY_FARMING_CORE.xpRequired(3)):
			RARITY_FARMING_CORE.levelup(DEVELOPER[1], 1, {"from": DEVELOPER[0]})
			print("\n" + Fore.GREEN + 'Level up!' + Style.RESET_ALL)

		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) >= 6) and (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 18) and (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 72) and (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) == 3):
			break
	
	WOOD_LOOT_0.approve(DEVELOPER[1], WOOD_FARMING_3.RARITY_EXTENDED_NCP(), 6, {"from": DEVELOPER[0]})
	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_3.RARITY_EXTENDED_NCP(), 18, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_3.RARITY_EXTENDED_NCP(), 72, {"from": DEVELOPER[0]})
	WOOD_FARMING_3.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n", Fore.GREEN + 'Tier 3 unlocked!' + Style.RESET_ALL)
	previousWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	previousWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	previousWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);

def runFarmFrom3To4():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4

	while True:
		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) < 6):
			WOOD_FARMING_0.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) < 18):
			WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) < 36):
			WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_3.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})

		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1

		if (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) < 4) and (RARITY_FARMING_CORE.xp(DEVELOPER[1], 1) >= RARITY_FARMING_CORE.xpRequired(4)):
			RARITY_FARMING_CORE.levelup(DEVELOPER[1], 1, {"from": DEVELOPER[0]})
			print("\n" + Fore.GREEN + 'Level up!' + Style.RESET_ALL)

		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) >= 6) and (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 18) and (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 36) and (WOOD_LOOT_3.balanceOf(DEVELOPER[1]) >= 120) and (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) == 4):
			break
	
	WOOD_LOOT_0.approve(DEVELOPER[1], WOOD_FARMING_4.RARITY_EXTENDED_NCP(), 6, {"from": DEVELOPER[0]})
	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_4.RARITY_EXTENDED_NCP(), 18, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_4.RARITY_EXTENDED_NCP(), 36, {"from": DEVELOPER[0]})
	WOOD_LOOT_3.approve(DEVELOPER[1], WOOD_FARMING_4.RARITY_EXTENDED_NCP(), 120, {"from": DEVELOPER[0]})
	WOOD_FARMING_4.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n", Fore.GREEN + 'Tier 4 unlocked!' + Style.RESET_ALL)
	previousWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	previousWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	previousWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);

def runFarmFrom4To5():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4

	while True:
		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) < 6):
			WOOD_FARMING_0.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) < 18):
			WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) < 36):
			WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_3.balanceOf(DEVELOPER[1]) < 60):
			WOOD_FARMING_3.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_4.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})

		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1

		if (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) < 5) and (RARITY_FARMING_CORE.xp(DEVELOPER[1], 1) >= RARITY_FARMING_CORE.xpRequired(5)):
			RARITY_FARMING_CORE.levelup(DEVELOPER[1], 1, {"from": DEVELOPER[0]})
			print("\n" + Fore.GREEN + 'Level up!' + Style.RESET_ALL)

		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) >= 6) and (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 18) and (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 36) and (WOOD_LOOT_3.balanceOf(DEVELOPER[1]) >= 60) and (WOOD_LOOT_4.balanceOf(DEVELOPER[1]) >= 180) and (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) == 5):
			break
	
	WOOD_LOOT_0.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 6, {"from": DEVELOPER[0]})
	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 18, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 36, {"from": DEVELOPER[0]})
	WOOD_LOOT_3.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 60, {"from": DEVELOPER[0]})
	WOOD_LOOT_4.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 180, {"from": DEVELOPER[0]})
	WOOD_FARMING_5.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n", Fore.GREEN + 'Tier 5 unlocked!' + Style.RESET_ALL)
	previousWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	previousWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	previousWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);

def runFarmFrom5To6():
	global days, previousWoodT0, previousWoodT1, previousWoodT2, previousWoodT3, previousWoodT4, previousWoodT5

	while True:
		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) < 6):
			WOOD_FARMING_0.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) < 18):
			WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) < 36):
			WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_3.balanceOf(DEVELOPER[1]) < 60):
			WOOD_FARMING_3.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		if (WOOD_LOOT_4.balanceOf(DEVELOPER[1]) < 90):
			WOOD_FARMING_4.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_5.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})

		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1

		if (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) < 6) and (RARITY_FARMING_CORE.xp(DEVELOPER[1], 1) >= RARITY_FARMING_CORE.xpRequired(6)):
			RARITY_FARMING_CORE.levelup(DEVELOPER[1], 1, {"from": DEVELOPER[0]})
			print("\n" + Fore.GREEN + 'Level up!' + Style.RESET_ALL)

		if (WOOD_LOOT_0.balanceOf(DEVELOPER[1]) >= 6) and (WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 18) and (WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 36) and (WOOD_LOOT_3.balanceOf(DEVELOPER[1]) >= 60) and (WOOD_LOOT_4.balanceOf(DEVELOPER[1]) >= 90) and (WOOD_LOOT_5.balanceOf(DEVELOPER[1]) >= 252) and (RARITY_FARMING_CORE.level(DEVELOPER[1], 1) == 6):
			break
	
	WOOD_LOOT_0.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 6, {"from": DEVELOPER[0]})
	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 18, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 36, {"from": DEVELOPER[0]})
	WOOD_LOOT_3.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 60, {"from": DEVELOPER[0]})
	WOOD_LOOT_4.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 90, {"from": DEVELOPER[0]})
	WOOD_LOOT_5.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 252, {"from": DEVELOPER[0]})
	WOOD_FARMING_6.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n", Fore.GREEN + 'Tier 6 unlocked!' + Style.RESET_ALL)
	previousWoodT0 = WOOD_LOOT_0.balanceOf(DEVELOPER[1]);
	previousWoodT1 = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousWoodT2 = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousWoodT3 = WOOD_LOOT_3.balanceOf(DEVELOPER[1]);
	previousWoodT4 = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	previousWoodT5 = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);



def main():
	print("=================================================================================")
	print("RARITY_EXTENDED_WOOD_LOOT_0: '" + Fore.GREEN + WOOD_LOOT_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_1: '" + Fore.GREEN + WOOD_LOOT_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_2: '" + Fore.GREEN + WOOD_LOOT_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_3: '" + Fore.GREEN + WOOD_LOOT_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_4: '" + Fore.GREEN + WOOD_LOOT_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_5: '" + Fore.GREEN + WOOD_LOOT_5.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_LOOT_6: '" + Fore.GREEN + WOOD_LOOT_6.address + Style.RESET_ALL + "',")

	print("RARITY_EXTENDED_FARM_CORE:   '" + Fore.GREEN + RARITY_FARMING_CORE.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_0: '" + Fore.GREEN + WOOD_FARMING_0.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_1: '" + Fore.GREEN + WOOD_FARMING_1.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_2: '" + Fore.GREEN + WOOD_FARMING_2.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_3: '" + Fore.GREEN + WOOD_FARMING_3.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_4: '" + Fore.GREEN + WOOD_FARMING_4.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_5: '" + Fore.GREEN + WOOD_FARMING_5.address + Style.RESET_ALL + "',")
	print("RARITY_EXTENDED_WOOD_FARM_6: '" + Fore.GREEN + WOOD_FARMING_6.address + Style.RESET_ALL + "',")
	print("=================================================================================")

	# runFarmFrom0To1()
	# runFarmFrom1To2()
	# runFarmFrom2To3()
	# runFarmFrom3To4()
	# runFarmFrom4To5()
	# runFarmFrom5To6()
	# printStatus()

