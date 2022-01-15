require("dotenv").config();
const { expect, use } = require('chai');
const { solidity } = require('ethereum-waffle');
const { deployments, ethers } = require('hardhat');
const RarityExtendedName = artifacts.require("rarity_extended_name");

use(solidity);

const	RARITY_ADDRESS = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
let		RARITY;

describe('Tests', () => {
	let		rarityExtendedName;
    let		user;
	let		adventurerPool = [];

    before(async () => {
        await deployments.fixture();
        [user, anotherUser] = await ethers.getSigners();
		RARITY = new ethers.Contract(RARITY_ADDRESS, [
			'function next_summoner() public view returns (uint)',
			'function summon(uint _class) external',
			'function setApprovalForAll(address operator, bool _approved) external',
		], user);
		rarityExtendedName = await RarityExtendedName.new()
    });

	
	it('should be possible to get the name of the contract', async function() {
		const	name = await rarityExtendedName.name();
		await	expect(name).to.be.equal('Rarity Extended Name');
	})

	it('should be possible to summon 1 adventurer', async function() {
		const	nextAdventurer = Number(await RARITY.next_summoner());
		await	(await RARITY.summon(1)).wait();
		adventurerPool.push(nextAdventurer);	
	})

	it('should be possible to set_name : John', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'John', {from: user.address})).not.to.be.reverted;
	})

	it('should not be possible to set_name : []382hdebnkjdnw187/', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], '[]382hdebnkjdnw187/', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name :    Hello', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], '   Hello', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : Hello   ', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'Hello   ', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : Hel  lo', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'Hel  lo', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : Hell0', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'Hell0', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : Hello-', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'Hello-', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : -Hello', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], '-Hello', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : H- ello', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'H- ello', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : He -llo', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'He -llo', {from: user.address})).to.be.reverted;
	})
	it('should not be possible to set_name : He--llo', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'He--llo', {from: user.address})).to.be.reverted;
	})
	it('should be possible to get the name of the Adventurer', async function() {
		const	names = await rarityExtendedName.get_name(adventurerPool[0]);
		expect(names).to.be.equal('John');
	})
	it('should be possible to unset the name of the Adventurer', async function() {
		await expect(rarityExtendedName.unset_name(adventurerPool[0], {from: user.address})).not.to.be.reverted;
	})
	it('should be possible to get the no name for the Adventurer', async function() {
		const	names = await rarityExtendedName.get_name(adventurerPool[0]);
		expect(names).to.be.equal('');
	})

	it('should be possible to set_name : John', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'John', {from: user.address})).not.to.be.reverted;
	})
	it('should be possible to get the name of the Adventurer', async function() {
		const	names = await rarityExtendedName.get_name(adventurerPool[0]);
		expect(names).to.be.equal('John');
	})
	it('should not be possible for another user to update the name of non-owned adventurer', async function() {
		await expect(rarityExtendedName.set_name(adventurerPool[0], 'Jane', {from: anotherUser.address})).to.be.reverted;
	})
});