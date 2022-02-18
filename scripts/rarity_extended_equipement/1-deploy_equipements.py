from colorama import Fore, Style
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
)

DEPLOYER = accounts.load('rarityextended')
RARITY_EXTENDED_OP_MS = '0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3'
RARITY_CRAFTING_ADDR = '0xf41270836dF4Db1D28F7fd0935270e3A603e78cC'
RARITY_CRAFTING_TYPE2_CODEX_ADDR = '0xf5114A952Aca3e9055a52a87938efefc8BB7878C'
RARITY_CRAFTING_TYPE3_CODEX_ADDR = '0xeE1a2EA55945223404d73C0BbE57f540BBAAD0D8'

def main():
	# Step 1 - Deploying the Farm contract
	WRAPPER = DEPLOYER.deploy(rarity_extended_equipement_wrapper)

	# Step 2 - Deploying the base slots
	ARMOR_HEAD = DEPLOYER.deploy(rarity_extended_equipement_armor_head, 2, 1, WRAPPER)
	ARMOR_BODY = DEPLOYER.deploy(rarity_extended_equipement_armor_body, 2, 2, WRAPPER)
	ARMOR_HAND = DEPLOYER.deploy(rarity_extended_equipement_armor_hand, 2, 3, WRAPPER)
	ARMOR_FOOT = DEPLOYER.deploy(rarity_extended_equipement_armor_foot, 2, 4, WRAPPER)
	PRIMARY_WEAPONS = DEPLOYER.deploy(rarity_extended_equipement_primary_weapon, 3, 5, WRAPPER)
	SECONDARY_WEAPONS = DEPLOYER.deploy(rarity_extended_equipement_secondary_weapon, 3, 6, WRAPPER)
	SHIELDS = DEPLOYER.deploy(rarity_extended_equipement_shield, 2, 101, WRAPPER)

	# Step 3 - Linking the slots
	WRAPPER.registerSlot(ARMOR_HEAD);
	WRAPPER.registerSlot(ARMOR_BODY);
	WRAPPER.registerSlot(ARMOR_HAND);
	WRAPPER.registerSlot(ARMOR_FOOT);
	WRAPPER.registerSlot(PRIMARY_WEAPONS);
	WRAPPER.registerSlot(SECONDARY_WEAPONS);
	WRAPPER.registerSlot(SHIELDS);

	# Step 4 - Adding a first set of approved equipements
	ARMOR_BODY.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)
	PRIMARY_WEAPONS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE3_CODEX_ADDR)
	SECONDARY_WEAPONS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE3_CODEX_ADDR)
	SHIELDS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)

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
