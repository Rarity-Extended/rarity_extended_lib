from brownie import (
	accounts, Contract,
	rarity_extended_equipement_wrapper,
	rarity_extended_equipement_armor_head,
	rarity_extended_equipement_armor_body,
	rarity_extended_equipement_armor_hand,
	rarity_extended_equipement_armor_foot,
	rarity_extended_equipement_primary_weapon,
	rarity_extended_equipement_secondary_weapon,
	rarity_extended_equipement_shield,

	theForestProxyItems,
	theForest_armor_codex,
	theForest_jewelry_codex,
	theForest_weapon_codex
)
deployer = accounts[0] # or accounts.load('rarityextended')

# Some of the address for Rarity
RARITY_MANIFEST_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
RARITY_CRAFTING_ADDR = '0xf41270836dF4Db1D28F7fd0935270e3A603e78cC'
RARITY_CRAFTING_TYPE2_CODEX_ADDR = '0xf5114A952Aca3e9055a52a87938efefc8BB7878C'
RARITY_CRAFTING_TYPE3_CODEX_ADDR = '0xeE1a2EA55945223404d73C0BbE57f540BBAAD0D8'
THE_FOREST_ADDR = '0x48e6F88F1Ab05677675dE9d14a705f8A137ea2bC'

# Deploying The Forest Items Codexes
THEFOREST_PROXY_ITEMS = deployer.deploy(theForestProxyItems)
THEFOREST_ARMOR_CODEX = deployer.deploy(theForest_armor_codex)
THEFOREST_JEWELRY_CODEX = deployer.deploy(theForest_jewelry_codex)
THEFOREST_WEAPONS_CODEX = deployer.deploy(theForest_weapon_codex)

# Deploying the Equipement system
RARITY_CRAFTING = Contract.from_explorer(RARITY_CRAFTING_ADDR);
THE_FOREST = Contract.from_explorer(THE_FOREST_ADDR);
RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR);
WRAPPER = deployer.deploy(rarity_extended_equipement_wrapper)
# Deploying the initial set of equipements
ARMOR_HEAD = deployer.deploy(rarity_extended_equipement_armor_head, 2, 1, WRAPPER)
ARMOR_BODY = deployer.deploy(rarity_extended_equipement_armor_body, 2, 2, WRAPPER)
ARMOR_HAND = deployer.deploy(rarity_extended_equipement_armor_hand, 2, 3, WRAPPER)
ARMOR_FOOT = deployer.deploy(rarity_extended_equipement_armor_foot, 2, 4, WRAPPER)
PRIMARY_WEAPONS = deployer.deploy(rarity_extended_equipement_primary_weapon, 3, 5, WRAPPER)
SECONDARY_WEAPONS = deployer.deploy(rarity_extended_equipement_secondary_weapon, 3, 6, WRAPPER)
SHIELDS = deployer.deploy(rarity_extended_equipement_shield, 2, 101, WRAPPER)
# Linking the slots, the wrapped and the contracts
WRAPPER.registerSlot(ARMOR_HEAD);
WRAPPER.registerSlot(ARMOR_BODY);
WRAPPER.registerSlot(ARMOR_HAND);
WRAPPER.registerSlot(ARMOR_FOOT);
WRAPPER.registerSlot(PRIMARY_WEAPONS);
WRAPPER.registerSlot(SECONDARY_WEAPONS);
WRAPPER.registerSlot(SHIELDS);

def stealItems():
	DEVELOPER = ['0x9E63B020ae098E73cF201EE1357EDc72DFEaA518', '636245']
	OWNER_OF_CRAFTED_SHIELD = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', '733580', '241']
	OWNER_OF_CRAFTED_SHIELD_2 = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', '733308', '239']
	OWNER_OF_CRAFTED_ARMOR = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', '998384', '245']
	OWNER_OF_CRAFTED_WEAPON = ['0xcA59B2035A32DD673eD1BbddD0908341DE171663', '1354632', '4516']
	OWNER_OF_CRAFTED_WEAPON2 = ['0xE3fDc2133845D20D53FbF38ef99194065eEdB5C6', '1486439', '4515']
	OWNER_OF_CRAFTED_WEAPON_2HANDED = ['0xebabaCb71E6bed4Cc388745eB4d232e3E99d7e2A', '1851612', '4520']
	OWNER_OF_CRAFTED_WEAPON_RANGED = ['0xEA017EcF13732146237E3DDf5d234E4C178179DF', '1317318', '4519']
	OWNER_OF_THE_FOREST_WEAPON = ['0x3daee7602D159517CD7FfF8968b93E40B90071c0', '193188', '10']
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_SHIELD[0], DEVELOPER[0], OWNER_OF_CRAFTED_SHIELD[2], {'from': OWNER_OF_CRAFTED_SHIELD[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_SHIELD_2[0], DEVELOPER[0], OWNER_OF_CRAFTED_SHIELD_2[2], {'from': OWNER_OF_CRAFTED_SHIELD_2[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_ARMOR[0], DEVELOPER[0], OWNER_OF_CRAFTED_ARMOR[2], {'from': OWNER_OF_CRAFTED_ARMOR[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON[2], {'from': OWNER_OF_CRAFTED_WEAPON[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON2[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON2[2], {'from': OWNER_OF_CRAFTED_WEAPON2[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON_2HANDED[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': OWNER_OF_CRAFTED_WEAPON_2HANDED[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON_RANGED[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': OWNER_OF_CRAFTED_WEAPON_RANGED[0]})
	THE_FOREST.transferFrom(OWNER_OF_THE_FOREST_WEAPON[1], DEVELOPER[1], OWNER_OF_THE_FOREST_WEAPON[2], {'from': OWNER_OF_THE_FOREST_WEAPON[0]})


def addRegistries():
	# Adding a first set of approved equipements
	ARMOR_BODY.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)
	PRIMARY_WEAPONS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE3_CODEX_ADDR)
	SECONDARY_WEAPONS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE3_CODEX_ADDR)
	SHIELDS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)
	PRIMARY_WEAPONS.addRegistry(THEFOREST_PROXY_ITEMS, THE_FOREST_ADDR, THEFOREST_WEAPONS_CODEX)

def printEnv():
	print("=================================================================================")
	print("RARITY_EQUIPEMENT_WRAPPER_ADDR: '" + WRAPPER.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_HEAD_ADDR: '" + ARMOR_HEAD.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_BODY_ADDR: '" + ARMOR_BODY.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_HAND_ADDR: '" + ARMOR_HAND.address + "',")
	print("RARITY_EQUIPEMENT_ARMOR_FOOT_ADDR: '" + ARMOR_FOOT.address + "',")
	print("RARITY_EQUIPEMENT_WEAPON_PRIMARY_ADDR: '" + PRIMARY_WEAPONS.address + "',")
	print("RARITY_EQUIPEMENT_WEAPON_SECONDARY_ADDR: '" + SECONDARY_WEAPONS.address + "',")
	print("RARITY_EQUIPEMENT_WEAPON_SHIELD: '" + SHIELDS.address + "',")
	print("=================================================================================")

def main():
	addRegistries()
	stealItems()
	printEnv()
