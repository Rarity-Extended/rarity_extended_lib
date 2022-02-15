from brownie import (
	accounts, chain, Contract,
	rarity_extended_basic_set,
)
deployer = accounts[0] # or accounts.load('rarityextended')
DEVELOPER = ['0x9E63B020ae098E73cF201EE1357EDc72DFEaA518', '635036']
RARITY_MANIFEST_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
BASIC_SET = deployer.deploy(rarity_extended_basic_set, RARITY_MANIFEST_ADDR, 3e18)

def printEnv():
	print("=================================================================================")
	print("RARITY_EXTENDED_EQUIPEMENT_BASIC_SET: '" + BASIC_SET.address + "',")
	print("=================================================================================")

def main():
	printEnv()

	BASIC_SET.buySet(10, DEVELOPER[1], {"from": DEVELOPER[0], "value": 1e18})
	assert BASIC_SET.ownerOf(1) == DEVELOPER[1]
	assert BASIC_SET.ownerOf(2) == DEVELOPER[1]
	assert BASIC_SET.ownerOf(3) == DEVELOPER[1]
	assert BASIC_SET.ownerOf(4) == DEVELOPER[1]
	assert BASIC_SET.ownerOf(5) == DEVELOPER[1]
	BASIC_SET.buySet(11, DEVELOPER[1], {"from": DEVELOPER[0], "value": 1e18})
