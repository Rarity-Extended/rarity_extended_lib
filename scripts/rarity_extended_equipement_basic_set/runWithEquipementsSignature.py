from eth_account import Account
from eth_account.messages import encode_structured_data

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

def chain_id():
    # BUG: hardhat provides mismatching chain.id and chainid()
    # https://github.com/trufflesuite/ganache/issues/1643
    return 1 if web3.clientVersion.startswith("HardhatNetwork") else chain.id

def sign(rERC721: Contract, owner: Account, operator, adventurer, to, tokenID, deadline: int = 0, override_nonce: int = None):
	name = "Basic Set"
	version = "1"
	if override_nonce:
		nonce = override_nonce
	else:
		nonce = BASIC_SET.nonces(adventurer)
	data = {
		"types": {
			"EIP712Domain": [
				{"name": "name", "type": "string"},
				{"name": "version", "type": "string"},
				{"name": "chainId", "type": "uint256"},
				{"name": "verifyingContract", "type": "address"},
			],
			"Permit": [
				{"name": "operator", "type": "uint"},
				{"name": "from", "type": "uint"},
				{"name": "to", "type": "uint"},
				{"name": "tokenId", "type": "uint"},
				{"name": "nonce", "type": "uint256"},
				{"name": "deadline", "type": "uint256"},
			],
		},
		"domain": {
			"name": name,
			"version": version,
			"chainId": 250,
			"verifyingContract": str(rERC721),
		},
		"primaryType": "Permit",
		"message": {
			"operator": operator,
			"from": adventurer,
			"to": to,
			"tokenId": tokenID,
			"nonce": nonce,
			"deadline": deadline,
		},
	}
	permit = encode_structured_data(data)
	return owner.sign_message(permit).signature


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
	user = Account.create()
	initEquipementSlots()

	chain.mine(10)
	adventurer = RARITY_MANIFEST.next_summoner()
	accounts[3].transfer(user.address, 10e18)
	RARITY_MANIFEST.summon(10, {"from": user.address})

	BASIC_SET = deployer.deploy(rarity_extended_basic_set, RARITY_MANIFEST_ADDR, 3e18)
	BASIC_SET.buySet(10, adventurer, {"from": user.address, "value": 3e18})
	assert BASIC_SET.ownerOf(1) == adventurer
	RARITY_MANIFEST.setApprovalForAll(ARMOR_HEAD, True, {'from': user.address}) # Bug with the forest, need approval for all

	ARMOR_HEAD.addRegistry(BASIC_SET, BASIC_SET, BASIC_SET_TYPE2_CODEX_ADDR)

	signature = sign(BASIC_SET, user, ARMOR_HEAD.RARITY_EXTENDED_NPC(), adventurer, ARMOR_HEAD.RARITY_EXTENDED_NPC(), 1)
	ARMOR_HEAD.set_rEquipement(
		adventurer,
		adventurer,
		BASIC_SET,
		1,
		0,
		signature,
		{'from': user.address}
	)