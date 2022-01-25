from brownie import Contract, accounts, convert

# 🏹 - Rarity Extended #########################################################
# This script is used to transfer the ownership of the loots contract from the
# developer address to the operational multisig address.
#
# Developer address is labeled as `rarityextended`.
# Multisig address is 0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3.
###############################################################################
RARITY_EXTENDED_OP_MS = '0xFaEc40354d9F43A57b58Dc2b5cffe41564D18BB3'

rERC20_ABI = [
	{"inputs": [], "name": "extended", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
	{"inputs": [], "name": "pendingExtended", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
	{"inputs":[{"internalType":"address","name":"_extended","type":"address"}],"name":"setExtended","outputs":[],"stateMutability":"nonpayable","type":"function"}
]

def main():
	deployer = accounts.load('rarityextended')
	loots = [
		("Mushroom", "0xcd80cE7E28fC9288e20b806ca53683a439041738"),
		("Berries", "0x9d6C92CCa7d8936ade0976282B82F921F7C50696"),
		("Meat", "0x95174B2c7E08986eE44D65252E3323A782429809"),
		("Wood", "0xdcE321D1335eAcc510be61c00a46E6CF05d6fAA1"),
		("Leather", "0xc5E80Eef433AF03E9380123C75231A08dC18C4B6"),
		("Tusks", "0x60bFaCc2F96f3EE847cA7D8cC713Ee40114be667"),
		("Candies", "0x18733f3C91478B122bd0880f41411efd9988D97E"),
	]

	for (name, address) in loots:
		Loot = Contract.from_abi(name, address, rERC20_ABI, deployer)
		if (Loot.extended() == deployer and Loot.pendingExtended() != RARITY_EXTENDED_OP_MS):
			print('Setting multisig as new extended for '+name+' ...')
			Loot.setExtended(convert.to_address(RARITY_EXTENDED_OP_MS))
