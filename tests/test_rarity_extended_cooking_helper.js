require("dotenv").config();
const { expect, use } = require('chai');
const { solidity } = require('ethereum-waffle');
const { deployments, ethers } = require('hardhat');
const {mintERC20, ERC20ABI} = require('./_test_utils.js');

const RarityExtendedCookingHelper = artifacts.require("rarity_extended_cooking_helper");

use(solidity);

const	RARITY_ADDR = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
const   RARITY_GOLD_ADDR = '0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2';
const	RARITY_COOKING_ADDR = '0x796D8e2B774470E5f2D455053742a94B7A3f6C3A';
const   RARITY_EXTENDED_MEAT_ADDR = '0x95174B2c7E08986eE44D65252E3323A782429809';
let		RARITY;
let		ADVENTURER_ID;


describe('Tests', () => {
	let		rarityExtendedCookingHelper;
    let		user;

    before(async () => {
        await deployments.fixture();
        [deployer, user] = await ethers.getSigners();

		/******************************************************************************************
		** Mint and prepare adventurer with lot of intel
		******************************************************************************************/
		RARITY = new ethers.Contract(RARITY_ADDR, [
			'function next_summoner() public view returns (uint)',
			'function summon(uint _class) external',
			'function setApprovalForAll(address operator, bool _approved) external',
			'function adventure(uint _summoner) external'
		], user);

		ADVENTURER_ID = Number(await RARITY.next_summoner());
		await (await RARITY.summon(1)).wait();
        await mintERC20(RARITY_GOLD_ADDR, ADVENTURER_ID, '80000000000000000000', 2);
        await mintERC20(RARITY_EXTENDED_MEAT_ADDR, ADVENTURER_ID, '4514', 8);
		rarityExtendedCookingHelper = await RarityExtendedCookingHelper.new(RARITY_COOKING_ADDR);

		MEAT = new ethers.Contract(RARITY_EXTENDED_MEAT_ADDR, ERC20ABI, user);
		GOLD_CONTRACT = new ethers.Contract(RARITY_GOLD_ADDR, ERC20ABI, user);
    });

	
	it('should be possible to get the name of the function', async function() {
		const	name = await rarityExtendedCookingHelper.name();
		await	expect(name).to.be.equal('Rarity Extended Cooking Helper');

	})

	it('Should be possible to cook', async function() {
		await (await RARITY.setApprovalForAll(rarityExtendedCookingHelper.address, true)).wait();
		await expect(
			rarityExtendedCookingHelper.cook(
				'0x19C469a03eF38378c9e354bFCa3D804AAF07571B',
				ADVENTURER_ID,
				ADVENTURER_ID,
				{from: user.address}
			)
		).not.to.be.reverted;
	});
});
