import time
from brownie import rarity_extended_cooking_helper, accounts, Contract

RARITY_EXTENDED_COOKING = '0x7474002fe5640d612c9a76cb0b6857932ff891e8'

# 🏹 - Rarity Extended #########################################################
# This script is used to deploy the Rarity Extended Cooking Helper contract.
#
# CookingHelper:					 0xFE23ea8C57Ee4f28E9C60cA09C512Ce80e90E6F5
# Deployment cost:												  0,2118015 FTM
###############################################################################
def deployWithDev():
	deployer = accounts.load('rarityextended')
	cookingHelper = deployer.deploy(
		rarity_extended_cooking_helper,
		RARITY_EXTENDED_COOKING,
		publish_source=True,
		gas_price='300 gwei'
	)
	time.sleep(5)
	rarity_extended_cooking_helper.publish_source(cookingHelper)

def main():
	deployWithDev()
