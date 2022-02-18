from colorama import Fore, Style
from brownie import (accounts, Contract, rarity_extended_farming_core)

DEPLOYER = accounts.load('rarityextended')
RARITY_EXTENDED_OP_MS = '0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3'

def main():
	# Step 1 - Deploying the Farm contract
	RARITY_FARMING_CORE = DEPLOYER.deploy(rarity_extended_farming_core, publish_source=True)
	rarity_extended_farming_core.publish_source(RARITY_FARMING_CORE)
	RARITY_FARMING_CORE = Contract.from_explorer("0x5A6bc1Ca56509d197e9504E0afa04c6FE901889e")
	# Step 2 - Setting extended to the OP multisig
	RARITY_FARMING_CORE.setExtended(RARITY_EXTENDED_OP_MS, {"from": DEPLOYER})

	print("=================================================================================")
	print("RARITY_EXTENDED_FARM_CORE:   '" + Fore.GREEN + RARITY_FARMING_CORE.address + Style.RESET_ALL + "',")
	print("=================================================================================")
