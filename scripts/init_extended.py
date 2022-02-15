from brownie import (
	accounts, Contract, web3, chain,
	rarity_extended_equipement_wrapper,
	rarity_extended_equipement_armor_head,
	rarity_extended_equipement_armor_body,
	rarity_extended_equipement_armor_hand,
	rarity_extended_equipement_armor_foot,
	rarity_extended_equipement_primary_weapon,
	rarity_extended_equipement_secondary_weapon,
	rarity_extended_equipement_shield,
	rarity_extended_basic_set,
	rarity_extended_basic_set_armor_codex,
	rarity_extended_basic_set_weapon_codex
)
deployer = accounts[0] # or accounts.load('rarityextended')
DEVELOPER = ['0x9E63B020ae098E73cF201EE1357EDc72DFEaA518', 635036]
SOMEONE_ELSE = ['0x631dFeDBe5DBa0e2a6537a2830b9BD1FFA4Ef93D', 456465]
RARITY_MANIFEST_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR);

# Deploying Equipements
WRAPPER = deployer.deploy(rarity_extended_equipement_wrapper)
ARMOR_HEAD = deployer.deploy(rarity_extended_equipement_armor_head, 2, 1, WRAPPER)
ARMOR_BODY = deployer.deploy(rarity_extended_equipement_armor_body, 2, 2, WRAPPER)
ARMOR_HAND = deployer.deploy(rarity_extended_equipement_armor_hand, 2, 3, WRAPPER)
ARMOR_FOOT = deployer.deploy(rarity_extended_equipement_armor_foot, 2, 4, WRAPPER)
PRIMARY_WEAPONS = deployer.deploy(rarity_extended_equipement_primary_weapon, 3, 5, WRAPPER)
SECONDARY_WEAPONS = deployer.deploy(rarity_extended_equipement_secondary_weapon, 3, 6, WRAPPER)
SHIELDS = deployer.deploy(rarity_extended_equipement_shield, 2, 101, WRAPPER)

# Deploying Basic Sets
BASIC_SET = deployer.deploy(rarity_extended_basic_set, RARITY_MANIFEST_ADDR, 3e18)
BASIC_SET_TYPE2_CODEX_ADDR = deployer.deploy(rarity_extended_basic_set_armor_codex)
BASIC_SET_TYPE3_CODEX_ADDR = deployer.deploy(rarity_extended_basic_set_weapon_codex)

def printEnv():
	print("=================================================================================")
	print("RARITY_EQUIPEMENT_WRAPPER_ADDR: '" + WRAPPER.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_HEAD_ADDR: '" + ARMOR_HEAD.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_BODY_ADDR: '" + ARMOR_BODY.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_HAND_ADDR: '" + ARMOR_HAND.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_FOOT_ADDR: '" + ARMOR_FOOT.address + "',")
	print("RARITY_EQUIPEMENT_WEAPON_PRIMARY_ADDR: '" + PRIMARY_WEAPONS.address + "',")
	print("RARITY_EQUIPEMENT_WEAPON_SECONDARY_ADDR: '" + SECONDARY_WEAPONS.address + "',")
	print("RARITY_EQUIPEMENT_WEAPON_SHIELD_ADDR: '" + SHIELDS.address + "',")
	print("RARITY_EXTENDED_EQUIPEMENT_BASIC_SET_ADDR: '" + BASIC_SET.address + "',")
	print("RARITY_EXTENDED_EQUIPEMENT_BASIC_SET_ARMOR_CODEX_ADDR: '" + BASIC_SET_TYPE2_CODEX_ADDR.address + "',")
	print("RARITY_EXTENDED_EQUIPEMENT_BASIC_SET_WEAPON_CODEX_ADDR: '" + BASIC_SET_TYPE3_CODEX_ADDR.address + "',")
	print("=================================================================================")

def main():
	printEnv()
	
	WRAPPER.registerSlot(ARMOR_HEAD);
	WRAPPER.registerSlot(ARMOR_BODY);
	WRAPPER.registerSlot(ARMOR_HAND);
	WRAPPER.registerSlot(ARMOR_FOOT);
	WRAPPER.registerSlot(PRIMARY_WEAPONS);
	WRAPPER.registerSlot(SECONDARY_WEAPONS);
	WRAPPER.registerSlot(SHIELDS);
	ARMOR_HEAD.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR)
	ARMOR_BODY.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR)
	ARMOR_HAND.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR)
	ARMOR_FOOT.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR)
	PRIMARY_WEAPONS.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE3_CODEX_ADDR)
	SECONDARY_WEAPONS.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE3_CODEX_ADDR)
	SHIELDS.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR)

# 0xb384C4e4428005e6daC814504A941935694b2C61
	# RARITY_MANIFEST.setApprovalForAll(WRAPPER, True, {'from': DEVELOPER[0]})
	# BASIC_SET.setApprovalForAll(DEVELOPER[1], WRAPPER.RARITY_EXTENDED_NCP(), True, {'from': DEVELOPER[0]})

	# # BASIC_SET.approve(DEVELOPER[1], ARMOR_HEAD.RARITY_EXTENDED_NCP(), 1, {'from': DEVELOPER[0]})
	# WRAPPER.set_rEquipement(
	# 	1,
	# 	DEVELOPER[1],
	# 	DEVELOPER[1],
	# 	BASIC_SET,
	# 	1,
	# 	{'from': DEVELOPER[0]}
	# )

	# WRAPPER.set_rEquipement(
	# 	4,
	# 	DEVELOPER[1],
	# 	DEVELOPER[1],
	# 	BASIC_SET,
	# 	4,
	# 	{'from': DEVELOPER[0]}
	# )

	# OWNER_OF_CRAFTED_ARMOR = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', 998384, 245]
	# RARITY_CRAFTING_ADDR = '0xf41270836dF4Db1D28F7fd0935270e3A603e78cC'
	# RARITY_CRAFTING = Contract.from_explorer(RARITY_CRAFTING_ADDR);
	# RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_ARMOR[0], DEVELOPER[0], OWNER_OF_CRAFTED_ARMOR[2], {'from': OWNER_OF_CRAFTED_ARMOR[0]})

	# RARITY_CRAFTING_TYPE2_CODEX_ADDR = '0xf5114A952Aca3e9055a52a87938efefc8BB7878C'
	# ARMOR_BODY.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)

	# RARITY_CRAFTING.setApprovalForAll(WRAPPER, True, {'from': DEVELOPER[0]})
	# WRAPPER.set_equipement(2, DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_ARMOR[2], {'from': DEVELOPER[0]})
	# assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_ARMOR[2]) == ARMOR_BODY



	# RARITY_MANIFEST.setApprovalForAll(ARMOR_HAND, True, {'from': DEVELOPER[0]})
	# BASIC_SET.approve(DEVELOPER[1], ARMOR_HAND.RARITY_EXTENDED_NCP(), 3, {'from': DEVELOPER[0]})
	# ARMOR_HAND.set_rEquipement(DEVELOPER[1], DEVELOPER[1], BASIC_SET, 3, {'from': DEVELOPER[0]})
