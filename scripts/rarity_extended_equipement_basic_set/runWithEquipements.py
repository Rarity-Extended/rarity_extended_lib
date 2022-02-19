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
BASIC_SET_TYPE2_CODEX_ADDR = deployer.deploy(rarity_extended_basic_set_armor_codex, publish_source=True)
BASIC_SET_TYPE3_CODEX_ADDR = deployer.deploy(rarity_extended_basic_set_weapon_codex, publish_source=True)

ARMOR_HEAD = Contract.from_explorer('0x494d46681f26DEEB93ba791aca975A77ac9CF917')
ARMOR_BODY = Contract.from_explorer('0xCCcD46478F384b1E49E3282a14e4431C7dD0D9c4')
ARMOR_HAND = Contract.from_explorer('0x7b562412Ba62141c6497eA6256c100b19F56a687')
ARMOR_FOOT = Contract.from_explorer('0x9578f6bB11B7f0E02ad9855d8F7A1B2972B8B881')
PRIMARY_WEAPONS = Contract.from_explorer('0x1A04fF6Db46dB1be64c3bC53f1481e197B5C82Af')
SECONDARY_WEAPONS = Contract.from_explorer('0x150c6F9A391cA9076F5f9Cf5e1D8A41c80540679')
SHIELDS = Contract.from_explorer('0x1a8B00725126e26638b88833Abfb08f6AdBa63f5')

ARMOR_HEAD.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR, {'from': deployer})
ARMOR_BODY.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR, {'from': deployer})
ARMOR_HAND.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR, {'from': deployer})
ARMOR_FOOT.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR, {'from': deployer})
PRIMARY_WEAPONS.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE3_CODEX_ADDR, {'from': deployer})
SECONDARY_WEAPONS.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE3_CODEX_ADDR, {'from': deployer})
SHIELDS.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR, {'from': deployer})



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

def initEquipementSlots():
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

def main():
	printEnv()
	initEquipementSlots()
	BASIC_SET = deployer.deploy(rarity_extended_basic_set, RARITY_MANIFEST_ADDR, 3e18)
	BASIC_SET.buySet(10, DEVELOPER[1], {"from": DEVELOPER[0], "value": 3e18})
	assert BASIC_SET.ownerOf(1) == DEVELOPER[1]
	RARITY_MANIFEST.setApprovalForAll(ARMOR_HEAD, True, {'from': DEVELOPER[0]}) # Bug with the forest, need approval for all

	ARMOR_HEAD.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR) #safe because not set sometimes

	ARMOR_HEAD.set_rEquipement(
		DEVELOPER[1],
		DEVELOPER[1],
		BASIC_SET,
		1,
		{'from': DEVELOPER[0]}
	)
