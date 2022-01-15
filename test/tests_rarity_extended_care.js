require("dotenv").config();
const { expect, use } = require('chai');
const { solidity } = require('ethereum-waffle');
const { deployments, ethers } = require('hardhat');
const RarityExtendedCare = artifacts.require("rarity_extended_care");

use(solidity);

const	RARITY_ADDRESS = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
let		RARITY;

describe('Tests', () => {
	let		rarityExtendedCare;
    let		user;
	let		adventurerPool = [];
	let		anotherAdventurerPool = [];
	let		againAnotherAdventurerPool = [];

    before(async () => {
        await deployments.fixture();
        [user, anotherUser] = await ethers.getSigners();
		RARITY = new ethers.Contract(RARITY_ADDRESS, [
			'function next_summoner() public view returns (uint)',
			'function summon(uint _class) external',
			'function setApprovalForAll(address operator, bool _approved) external',
			'function xp(uint _summoner) external view returns (uint)',
			'function adventurers_log(uint adventurer) external view returns (uint)'
		], user);
		rarityExtendedCare = await RarityExtendedCare.new()
    });

	
	it('should be possible to get the name of the function', async function() {
		const	name = await rarityExtendedCare.name();
		await	expect(name).to.be.equal('Rarity Extended Care');
	})

	it('should be possible to summon 12 adventurers', async function() {
		for (let index = 1; index < 12; index++) {
			const	nextAdventurer = Number(await RARITY.next_summoner());
			await	(await RARITY.summon(index)).wait();
			adventurerPool.push(nextAdventurer);	
		}
	})

	it('should be possible approveForAll', async function() {
		const receipt = await (await RARITY.setApprovalForAll(rarityExtendedCare.address, true)).wait();
		await	expect(receipt?.status).to.be.eq(1);
	})

	it('should be possible to careOf for all', async function() {
		await expect(rarityExtendedCare.care_of(
			adventurerPool,
			[true, true, true, true],
			0,
			{from: user.address}
		)).not.to.be.reverted;
	})

	it('the careOf should have had an effect', async function() {
		for (let index = 1; index < 12; index++) {
			const xp = await RARITY.xp(adventurerPool[index - 1])
			const log = await RARITY.adventurers_log(adventurerPool[index - 1])

			await expect(Number(xp)).to.be.gt(0);
			await expect(Number(log)).not.to.be.eq(0);
		}
	})

	it('should be possible to summon 12 other adventurers', async function() {
		for (let index = 1; index < 12; index++) {
			const	nextAdventurer = Number(await RARITY.next_summoner());
			await	(await RARITY.summon(index)).wait();
			anotherAdventurerPool.push(nextAdventurer);	
		}
	})

	it('should not be possible to careOf for all with another user', async function() {
		await expect(rarityExtendedCare.care_of(
			adventurerPool,
			[true, true, true, true],
			0,
			{from: anotherUser.address}
		)).to.be.reverted;
	})

	it('should be possible to approve another user', async function() {
		await expect(rarityExtendedCare.setAllowance(
			anotherAdventurerPool,
			anotherUser.address,
			true,
			{from: user.address}
		)).not.to.be.reverted;
	})

	it('should be possible to careOf for all with another user', async function() {
		await expect(rarityExtendedCare.care_of(
			anotherAdventurerPool,
			[true, true, true, true],
			0,
			{from: anotherUser.address}
		)).not.to.be.reverted;
	})

	it('the careOf should have had an effect', async function() {
		for (let index = 1; index < 12; index++) {
			const xp = await RARITY.xp(anotherAdventurerPool[index - 1])
			const log = await RARITY.adventurers_log(anotherAdventurerPool[index - 1])

			await expect(Number(xp)).to.be.gt(0);
			await expect(Number(log)).not.to.be.eq(0);
		}
	})

	it('should be possible to remove approve of the another user', async function() {
		await expect(rarityExtendedCare.setAllowance(
			anotherAdventurerPool,
			anotherUser.address,
			false,
			{from: user.address}
		)).not.to.be.reverted;
	})

	it('should not be possible to careOf for all with another user', async function() {
		await expect(rarityExtendedCare.care_of(
			adventurerPool,
			[true, true, true, true],
			0,
			{from: anotherUser.address}
		)).to.be.reverted;
	})

	it('should be possible to summon again another 12 adventurers', async function() {
		for (let index = 1; index < 12; index++) {
			const	nextAdventurer = Number(await RARITY.next_summoner());
			await	(await RARITY.summon(index)).wait();
			againAnotherAdventurerPool.push(nextAdventurer);	
		}
	})

	it('should be possible to adventure for all', async function() {
		await expect(rarityExtendedCare.adventure(
			againAnotherAdventurerPool,
			{from: user.address}
		)).not.to.be.reverted;
	})
	it('should be possible to adventure_cellar for all', async function() {
		await expect(rarityExtendedCare.adventure_cellar(
			againAnotherAdventurerPool,
			1,
			{from: user.address}
		)).not.to.be.reverted;
	})
	it('should be possible to level_up for all', async function() {
		await expect(rarityExtendedCare.level_up(
			againAnotherAdventurerPool,
			{from: user.address}
		)).not.to.be.reverted;
	})
	it('should be possible to claim_gold for all', async function() {
		await expect(rarityExtendedCare.claim_gold(
			againAnotherAdventurerPool,
			{from: user.address}
		)).not.to.be.reverted;
	})
});