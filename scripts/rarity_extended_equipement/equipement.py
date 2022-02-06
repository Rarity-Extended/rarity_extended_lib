import pytest
import brownie
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

# Some Addresses to use for the tests
DEVELOPER = ['0x9E63B020ae098E73cF201EE1357EDc72DFEaA518', '636245']
OWNER_OF_CRAFTED_SHIELD = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', '733580', '241']
OWNER_OF_CRAFTED_SHIELD_2 = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', '733308', '239']
OWNER_OF_CRAFTED_ARMOR = ['0xDeA98C16E02dDC053EfEf2C75ca7B42f2DB6c678', '998384', '245']
OWNER_OF_CRAFTED_WEAPON = ['0xcA59B2035A32DD673eD1BbddD0908341DE171663', '1354632', '4516']
OWNER_OF_CRAFTED_WEAPON2 = ['0xE3fDc2133845D20D53FbF38ef99194065eEdB5C6', '1486439', '4515']
OWNER_OF_CRAFTED_WEAPON_2HANDED = ['0xebabaCb71E6bed4Cc388745eB4d232e3E99d7e2A', '1851612', '4520']
OWNER_OF_CRAFTED_WEAPON_RANGED = ['0xEA017EcF13732146237E3DDf5d234E4C178179DF', '1317318', '4519']
OWNER_OF_THE_FOREST_WEAPON = ['0x3daee7602D159517CD7FfF8968b93E40B90071c0', '193188', '10']

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
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_SHIELD[0], DEVELOPER[0], OWNER_OF_CRAFTED_SHIELD[2], {'from': OWNER_OF_CRAFTED_SHIELD[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_SHIELD_2[0], DEVELOPER[0], OWNER_OF_CRAFTED_SHIELD_2[2], {'from': OWNER_OF_CRAFTED_SHIELD_2[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_ARMOR[0], DEVELOPER[0], OWNER_OF_CRAFTED_ARMOR[2], {'from': OWNER_OF_CRAFTED_ARMOR[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON[2], {'from': OWNER_OF_CRAFTED_WEAPON[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON2[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON2[2], {'from': OWNER_OF_CRAFTED_WEAPON2[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON_2HANDED[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': OWNER_OF_CRAFTED_WEAPON_2HANDED[0]})
	RARITY_CRAFTING.safeTransferFrom(OWNER_OF_CRAFTED_WEAPON_RANGED[0], DEVELOPER[0], OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': OWNER_OF_CRAFTED_WEAPON_RANGED[0]})
	THE_FOREST.transferFrom(OWNER_OF_THE_FOREST_WEAPON[1], DEVELOPER[1], OWNER_OF_THE_FOREST_WEAPON[2], {'from': OWNER_OF_THE_FOREST_WEAPON[0]})


# 🏹 - Rarity Extended #############################################################################
# This script will check the revert in all the default situations (not approved, invalid type,
# etc.). Shield are used as default equipement.
###################################################################################################
def checkSituations():
	# ❌ - REVERT CHECKER ##########################################################################
	# With no previous approve, it should not be possible to set the equipement.
	# The revert message should be: "ERC721: transfer caller is not owner nor approved"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='ERC721: transfer caller is not owner nor approved'):
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With an invalid registry, it should not be possible to set the equipement.
	# The revert message should be: "registered"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!registered'):
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_MANIFEST_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a non owned adventurer, it should not be possible to set the equipement.
	# The revert message should be: "!owner"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!owner'):
		SHIELDS.set_equipement('123456', DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a non approved operator, it should not be possible to set the equipement.
	# The revert message should be: "!owner"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!owner'):
		SHIELDS.set_equipement('123456', '0x91BCCDe439e5a00EBaE0B883Ac0d527929718c24', RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a non owned item, it should not be possible to set the equipement.
	# The revert message should be: "!equipement"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!equipement'):
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, 123, {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a non compatible item type, it should not be possible to set the equipement.
	# The revert message should be: "!base_type"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!base_type'):
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a an already equiped shield, it should not be possible to set the equipement.
	# The revert message should be: "!already_equiped"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!already_equiped'):
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD[2]) == SHIELDS
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD_2[2]) == DEVELOPER[0]

# 🏹 - Rarity Extended #############################################################################
# This script will check the revert in all the specific body equipement situations.
# It will also try to set and uset the equipement.
###################################################################################################
def checkSpecificSituationsBody():
	# ❌ - REVERT CHECKER ##########################################################################
	# With a shield as armor, it should not be possible to set the equipement.
	# The revert message should be: "!shield"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!shield'):
		RARITY_CRAFTING.approve(ARMOR_BODY, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		ARMOR_BODY.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})

	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with an actual armor.
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(ARMOR_BODY, OWNER_OF_CRAFTED_ARMOR[2], {'from': DEVELOPER[0]})
	ARMOR_BODY.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_ARMOR[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_ARMOR[2]) == ARMOR_BODY
	ARMOR_BODY.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_ARMOR[2]) == DEVELOPER[0]

# 🏹 - Rarity Extended #############################################################################
# This script will check the revert in all the specific primary weapon equipement situations.
# It will also try to set and uset the equipement.
###################################################################################################
def checkSpecificSituationsPrimaryWeapon():
	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a any weapon
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == PRIMARY_WEAPONS
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == DEVELOPER[0]

	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a any one handed weapon and a shield
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
	SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
	RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == PRIMARY_WEAPONS
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == DEVELOPER[0]
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a shield equiped, it should not be possible to set the ranged equipement.
	# The revert message should be: "!shield"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!shield'):
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
		PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a shield equiped, it should not be possible to set the 2handed equipement.
	# The revert message should be: "!shield"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!shield'):
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
		PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD[2]) == DEVELOPER[0]

# 🏹 - Rarity Extended #############################################################################
# This script will check the revert in all the specific secondary weapon equipement situations.
# It will also try to set and uset the equipement.
###################################################################################################
def checkSpecificSituationsSecondaryWeapon():
	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a any weapon
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == SECONDARY_WEAPONS
	SECONDARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == DEVELOPER[0]

	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a any one handed weapon and a secondary weapon
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON2[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON2[2], {'from': DEVELOPER[0]})

	RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == SECONDARY_WEAPONS
	SECONDARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == DEVELOPER[0]
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON2[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a 2 handed primary weapon equiped, it should not be possible to set the equipement.
	# The revert message should be: "!primary_encumbrance"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!primary_encumbrance'):
		RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
		PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
		SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON_2HANDED[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a ranged primary weapon equiped, it should not be possible to set the equipement.
	# The revert message should be: "!primary_encumbrance"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!primary_encumbrance'):
		RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
		PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
		SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON_RANGED[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a 2handed equipement, it should not be possible to set the equipement.
	# The revert message should be: "!encumbrance"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!encumbrance'):
		RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
		SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a ranged equipement, it should not be possible to set the equipement.
	# The revert message should be: "!encumbrance"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!encumbrance'):
		RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
		SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})

	# ❌ - REVERT CHECKER ##########################################################################
	# With a shield equiped, it should not be possible to set the equipement.
	# The revert message should be: "!shield"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!shield'):
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD[2], {'from': DEVELOPER[0]})
		SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON[2], {'from': DEVELOPER[0]})
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD[2]) == DEVELOPER[0]

# 🏹 - Rarity Extended #############################################################################
# This script will check the revert in all the specific shield equipement situations.
# It will also try to set and uset the equipement.
###################################################################################################
def checkSpecificSituationsShield():
	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a shield
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD_2[2]) == SHIELDS
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD_2[2]) == DEVELOPER[0]

	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a any one handed weapon and a shield
	# Should be able to set and unset equipement
	###############################################################################################
	RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON2[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON2[2], {'from': DEVELOPER[0]})
	RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_SHIELD_2[2]) == SHIELDS
	SHIELDS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON[2]) == DEVELOPER[0]
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON2[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a 2 handed primary weapon equiped, it should not be possible to set the shield.
	# The revert message should be: "!primary_encumbrance"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!primary_encumbrance'):
		RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
		PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_2HANDED[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON_2HANDED[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a ranged primary weapon equiped, it should not be possible to set the shield.
	# The revert message should be: "!primary_encumbrance"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!primary_encumbrance'):
		RARITY_CRAFTING.approve(PRIMARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
		PRIMARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON_RANGED[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON_RANGED[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With a secondary weapon, it should not be possible to set the equipement.
	# The revert message should be: "!secondary_weapon"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!secondary_weapon'):
		RARITY_CRAFTING.approve(SECONDARY_WEAPONS, OWNER_OF_CRAFTED_WEAPON2[2], {'from': DEVELOPER[0]})
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
		SECONDARY_WEAPONS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_WEAPON2[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_SHIELD_2[2], {'from': DEVELOPER[0]})
	SECONDARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert RARITY_CRAFTING.ownerOf(OWNER_OF_CRAFTED_WEAPON2[2]) == DEVELOPER[0]

	# ❌ - REVERT CHECKER ##########################################################################
	# With an armor not a shield, it should not be possible to set the equipement.
	# The revert message should be: "!shield"
	###############################################################################################
	with pytest.raises(brownie.exceptions.VirtualMachineError, match='!shield'):
		RARITY_CRAFTING.approve(SHIELDS, OWNER_OF_CRAFTED_ARMOR[2], {'from': DEVELOPER[0]})
		SHIELDS.set_equipement(DEVELOPER[1], DEVELOPER[0], RARITY_CRAFTING_ADDR, OWNER_OF_CRAFTED_ARMOR[2], {'from': DEVELOPER[0]})


# 🏹 - Rarity Extended #############################################################################
# This script will check the revert in all the specific primary weapon equipement situations.
# It will also try to set and uset the equipement.
###################################################################################################
def checkPrimaryWeaponRarity():
	# ✅ - SUCCESS CHECKER #########################################################################
	# Should be successful with a any weapon
	# Should be able to set and unset equipement
	###############################################################################################
	PRIMARY_WEAPONS_MANAGER = PRIMARY_WEAPONS.RARITY_EXTENDED_NCP()
	THE_FOREST.approve(DEVELOPER[1], PRIMARY_WEAPONS_MANAGER, OWNER_OF_THE_FOREST_WEAPON[2], {'from': DEVELOPER[0]})
	RARITY_MANIFEST.setApprovalForAll(PRIMARY_WEAPONS, True, {'from': DEVELOPER[0]}) # Bug with the forest, need approval for all

	PRIMARY_WEAPONS.set_rEquipement(DEVELOPER[1], DEVELOPER[1], THEFOREST_PROXY_ITEMS, OWNER_OF_THE_FOREST_WEAPON[2], {'from': DEVELOPER[0]})
	assert THE_FOREST.ownerOf(OWNER_OF_THE_FOREST_WEAPON[2]) == PRIMARY_WEAPONS_MANAGER
	PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
	assert THE_FOREST.ownerOf(OWNER_OF_THE_FOREST_WEAPON[2]) == DEVELOPER[1]

def deployWithDev():
	# Adding a first set of approved equipements
	ARMOR_BODY.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)
	PRIMARY_WEAPONS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE3_CODEX_ADDR)
	SECONDARY_WEAPONS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE3_CODEX_ADDR)
	SHIELDS.addRegistry(RARITY_CRAFTING_ADDR, RARITY_CRAFTING_ADDR, RARITY_CRAFTING_TYPE2_CODEX_ADDR)
	PRIMARY_WEAPONS.addRegistry(THEFOREST_PROXY_ITEMS, THE_FOREST_ADDR, THEFOREST_WEAPONS_CODEX)

	# Perform basic checks, will be the same for every contract because based on the same BASE
	# checkSituations()
	# checkSpecificSituationsBody()
	# checkSpecificSituationsPrimaryWeapon()
	# checkSpecificSituationsSecondaryWeapon()
	# checkSpecificSituationsShield()

	# checkPrimaryWeaponRarity()

def main():
	stealItems()
	deployWithDev()























# deployer = accounts[0] # or accounts.load('rarityextended')

# # Some of the address for Rarity
# RARITY_MANIFEST_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
# THE_FOREST_ADDR = '0x48e6F88F1Ab05677675dE9d14a705f8A137ea2bC'

# # Some Addresses to use for the tests
# DEVELOPER = ['0x9E63B020ae098E73cF201EE1357EDc72DFEaA518', '636245']
# OWNER_OF_THE_FOREST_WEAPON = ['0x3daee7602D159517CD7FfF8968b93E40B90071c0', '193188', '10']

# # Deploying The Forest Items Codexes
# THEFOREST_PROXY_ITEMS = deployer.deploy(theForestProxyItems)
# THEFOREST_ARMOR_CODEX = deployer.deploy(theForest_armor_codex)
# THEFOREST_JEWELRY_CODEX = deployer.deploy(theForest_jewelry_codex)
# THEFOREST_WEAPONS_CODEX = deployer.deploy(theForest_weapon_codex)

# # Deploying the Equipement system
# THE_FOREST = Contract.from_explorer(THE_FOREST_ADDR);
# RARITY_MANIFEST = Contract.from_explorer(RARITY_MANIFEST_ADDR);

# WRAPPER = deployer.deploy(rarity_extended_equipement_wrapper)
# # Deploying the initial set of equipements
# PRIMARY_WEAPONS = deployer.deploy(rarity_extended_equipement_primary_weapon, 3, 5, WRAPPER)
# SECONDARY_WEAPONS = deployer.deploy(rarity_extended_equipement_secondary_weapon, 3, 6, WRAPPER)
# SHIELDS = deployer.deploy(rarity_extended_equipement_shield, 2, 101, WRAPPER)
# # Linking the slots, the wrapped and the contracts
# WRAPPER.registerSlot(5, PRIMARY_WEAPONS);
# WRAPPER.registerSlot(6, SECONDARY_WEAPONS);
# WRAPPER.registerSlot(101, SHIELDS);

# PRIMARY_WEAPONS.addRegistry(THEFOREST_PROXY_ITEMS, THE_FOREST_ADDR, THEFOREST_WEAPONS_CODEX)
# THE_FOREST.transferFrom(OWNER_OF_THE_FOREST_WEAPON[1], DEVELOPER[1], OWNER_OF_THE_FOREST_WEAPON[2], {'from': OWNER_OF_THE_FOREST_WEAPON[0]})



# PRIMARY_WEAPONS_MANAGER = PRIMARY_WEAPONS.RARITY_EXTENDED_NCP()
# THE_FOREST.approve(DEVELOPER[1], PRIMARY_WEAPONS_MANAGER, OWNER_OF_THE_FOREST_WEAPON[2], {'from': DEVELOPER[0]})
# RARITY_MANIFEST.setApprovalForAll(PRIMARY_WEAPONS, True, {'from': DEVELOPER[0]}) # Bug with the forest, need approval for all
# RARITY_MANIFEST.setApprovalForAll(THE_FOREST, True, {'from': DEVELOPER[0]}) # Bug with the forest, need approval for all

# PRIMARY_WEAPONS.set_rEquipement(DEVELOPER[1], DEVELOPER[1], THEFOREST_PROXY_ITEMS, OWNER_OF_THE_FOREST_WEAPON[2], {'from': DEVELOPER[0]})
# assert THE_FOREST.ownerOf(OWNER_OF_THE_FOREST_WEAPON[2]) == PRIMARY_WEAPONS_MANAGER
# tx = PRIMARY_WEAPONS.unset_equipement(DEVELOPER[1], {'from': DEVELOPER[0]})
# assert THE_FOREST.ownerOf(OWNER_OF_THE_FOREST_WEAPON[2]) == DEVELOPER[1]




# # function _isApprovedOrOwnerOfSummoner(uint _summoner) internal view returns (bool) {
# # 	return
# # 	rm.getApproved(_summoner) == msg.sender ||
# # 	rm.ownerOf(_summoner) == msg.sender ||
# # 	rm.isApprovedForAll(
# # 		rm.ownerOf(_summoner), msg.sender
# # 	);
# # }