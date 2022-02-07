from colorama import Fore, Back, Style
from brownie import (
	accounts, Contract, chain, convert,
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
WRAPPER = deployer.deploy(rarity_extended_farming_wrapper)
RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR)

# Deploying the Loots address
WOOD_LOOT_1 = Contract.from_explorer(RARITY_EXTENDED_WOOD_LOOT_ADDR)
WOOD_LOOT_2 = deployer.deploy(Loot, "Soft Wood", "Soft Wood - (Loot)")
WOOD_LOOT_3 = deployer.deploy(Loot, "Fine Wood", "Fine Wood - (Loot)")
WOOD_LOOT_4 = deployer.deploy(Loot, "Seasoned Wood", "Seasoned Wood - (Loot)")
WOOD_LOOT_5 = deployer.deploy(Loot, "Hard Wood", "Hard Wood - (Loot)")
WOOD_LOOT_6 = deployer.deploy(Loot, "Elder Wood", "Elder Wood - (Loot)")
WOOD_LOOT_7 = deployer.deploy(Loot, "Ancient Wood", "Ancient Wood - (Loot)")


# Deploying the initial set of farming
WOOD_FARMING_1 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_1.address, "Rarity Wood", 0, [], [])
WOOD_FARMING_2 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_2.address, "Rarity Soft Wood", 1,
	[WOOD_LOOT_1], [12]
)
WOOD_FARMING_3 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_3.address, "Rarity Fine Wood", 1,
	[WOOD_LOOT_1, WOOD_LOOT_2], [6, 36]
)
WOOD_FARMING_4 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_4.address, "Rarity Seasoned Wood", 2,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3], [6, 18, 72]
)
WOOD_FARMING_5 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_5.address, "Rarity Hard Wood", 4,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4], [6, 18, 36, 120]
)
WOOD_FARMING_6 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_6.address, "Rarity Elder Wood", 8,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4, WOOD_LOOT_5], [6, 18, 36, 60, 180]
)
WOOD_FARMING_7 = deployer.deploy(rarity_extended_farming_base, 1, WRAPPER, WOOD_LOOT_7.address, "Rarity Ancient Wood", 16,
	[WOOD_LOOT_1, WOOD_LOOT_2, WOOD_LOOT_3, WOOD_LOOT_4, WOOD_LOOT_5, WOOD_LOOT_6], [6, 18, 36, 60, 90, 252]
)


# Set the farming as loot minters
WOOD_LOOT_1.setMinter(WOOD_FARMING_1, {"from": RARITY_EXTENDED_WOOD_LOOT_MINTER_ADDR})
WOOD_LOOT_2.setMinter(WOOD_FARMING_2, {"from": deployer})
WOOD_LOOT_3.setMinter(WOOD_FARMING_3, {"from": deployer})
WOOD_LOOT_4.setMinter(WOOD_FARMING_4, {"from": deployer})
WOOD_LOOT_5.setMinter(WOOD_FARMING_5, {"from": deployer})
WOOD_LOOT_6.setMinter(WOOD_FARMING_6, {"from": deployer})
WOOD_LOOT_7.setMinter(WOOD_FARMING_7, {"from": deployer})

# Linking the slots, the wrapped and the contracts
WRAPPER.registerFarm(WOOD_FARMING_1);
WRAPPER.registerFarm(WOOD_FARMING_2);
WRAPPER.registerFarm(WOOD_FARMING_3);
WRAPPER.registerFarm(WOOD_FARMING_4);
WRAPPER.registerFarm(WOOD_FARMING_5);
WRAPPER.registerFarm(WOOD_FARMING_6);
WRAPPER.registerFarm(WOOD_FARMING_7);

days = 0
previousWOOD = 0
previousSOFT_WOOD = 0
previousSEASONED_WOOD = 0
previousHARD_WOOD = 0

def printStatus():
	global days, previousWOOD, previousSOFT_WOOD, previousSEASONED_WOOD, previousHARD_WOOD

	_totalWood = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	_earnedWood = _totalWood - previousWOOD
	previousWOOD = _totalWood

	_totalSoftWood = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	_earnedSoftWood = _totalSoftWood - previousSOFT_WOOD
	previousSOFT_WOOD = _totalSoftWood

	_totalSeasonedWood = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	_earnedSeasonedWood = _totalSeasonedWood - previousSEASONED_WOOD
	previousSEASONED_WOOD = _totalSeasonedWood

	_totalHardWood = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);
	_earnedHardWood = _totalHardWood - previousHARD_WOOD
	previousHARD_WOOD = _totalHardWood
	print("\n=================================================================================")
	print("WOOD: " + convert.to_string(_totalWood), end="")
	if (_earnedWood > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedWood) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("SOFT_WOOD: " + convert.to_string(_totalSoftWood), end="")
	if (_earnedSoftWood > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedSoftWood) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("SEASONED_WOOD: " + convert.to_string(_totalSeasonedWood), end="")
	if (_earnedSeasonedWood > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedSeasonedWood) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("HARD_WOOD: " + convert.to_string(_totalHardWood), end="")
	if (_earnedHardWood > 0):
		print(Fore.GREEN + ' (+' + convert.to_string(_earnedHardWood) + ')' + Style.RESET_ALL)
	else:
		print('')

	print("XP: " + convert.to_string(WRAPPER.xp(DEVELOPER[1], 1)))
	print("DAYS: " + convert.to_string(days))
	print("=================================================================================")

def runFarm():
	global days, previousWOOD, previousSOFT_WOOD, previousSEASONED_WOOD, previousHARD_WOOD

	###########################################################################
	# Loop to farm some WOOD_1 for a few days
	###########################################################################
	while True:
		WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1
		if WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 50:
			break
	
	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_2.RARITY_EXTENDED_NCP(), 50, {"from": DEVELOPER[0]})
	WOOD_FARMING_2.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})
	print("\n=================================================================================")
	print("UNLOCKING LVL 2")
	previousWOOD = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousSOFT_WOOD = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousSEASONED_WOOD = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	previousHARD_WOOD = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);
	print("=================================================================================")

	###########################################################################
	# Loop to farm some WOOD_1 and WOOD_2 for a few days
	###########################################################################
	while True:
		WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1
		if WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 100 and WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 80:
			break

	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_4.RARITY_EXTENDED_NCP(), 100, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_4.RARITY_EXTENDED_NCP(), 80, {"from": DEVELOPER[0]})
	WOOD_FARMING_4.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n=================================================================================")
	print("UNLOCKING LVL 3")
	previousWOOD = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousSOFT_WOOD = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousSEASONED_WOOD = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	previousHARD_WOOD = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);
	print("=================================================================================")

	###########################################################################
	# Loop to farm some WOOD_1, WOOD_2 and WOOD_3 for a few days
	###########################################################################
	while True:
		WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_4.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1
		if WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 200 and WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 160 and WOOD_LOOT_4.balanceOf(DEVELOPER[1]) >= 115:
			break

	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 200, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 160, {"from": DEVELOPER[0]})
	WOOD_LOOT_4.approve(DEVELOPER[1], WOOD_FARMING_5.RARITY_EXTENDED_NCP(), 100, {"from": DEVELOPER[0]})
	WOOD_FARMING_5.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n=================================================================================")
	print("UNLOCKING LVL 4")
	previousWOOD = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousSOFT_WOOD = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousSEASONED_WOOD = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	previousHARD_WOOD = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);
	print("=================================================================================")

	###########################################################################
	# Loop to farm some WOOD_1, WOOD_2, WOOD_3 and WOOD_4 for a few days
	###########################################################################
	while True:
		WOOD_FARMING_1.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_2.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_4.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		WOOD_FARMING_5.harvest(DEVELOPER[1], {"from": DEVELOPER[0]})
		printStatus()
		chain.sleep((86400 * 1) + 3600)
		chain.mine()
		days += 1
		if WOOD_LOOT_1.balanceOf(DEVELOPER[1]) >= 300 and WOOD_LOOT_2.balanceOf(DEVELOPER[1]) >= 200 and WOOD_LOOT_4.balanceOf(DEVELOPER[1]) >= 150 and WOOD_LOOT_5.balanceOf(DEVELOPER[1]) >= 115:
			break

	WOOD_LOOT_1.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 300, {"from": DEVELOPER[0]})
	WOOD_LOOT_2.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 240, {"from": DEVELOPER[0]})
	WOOD_LOOT_4.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 200, {"from": DEVELOPER[0]})
	WOOD_LOOT_5.approve(DEVELOPER[1], WOOD_FARMING_6.RARITY_EXTENDED_NCP(), 100, {"from": DEVELOPER[0]})
	WOOD_FARMING_6.unlock(DEVELOPER[1], {"from": DEVELOPER[0]})

	print("\n=================================================================================")
	print("UNLOCKING LVL 5")
	previousWOOD = WOOD_LOOT_1.balanceOf(DEVELOPER[1]);
	previousSOFT_WOOD = WOOD_LOOT_2.balanceOf(DEVELOPER[1]);
	previousSEASONED_WOOD = WOOD_LOOT_4.balanceOf(DEVELOPER[1]);
	previousHARD_WOOD = WOOD_LOOT_5.balanceOf(DEVELOPER[1]);
	print("=================================================================================")

	printStatus()


def main():
	printEnv()
	runFarm()
