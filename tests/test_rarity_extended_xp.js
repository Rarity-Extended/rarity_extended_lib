require("dotenv").config();
const { expect, use } = require('chai');
const { solidity } = require('ethereum-waffle');
const { deployments, ethers } = require('hardhat');
const RarityXPProxy = artifacts.require("rarity_xp_proxy");
const RarityXPProxySpender = artifacts.require("dummy_rarity_extended_xp_spender");

use(solidity);

const	RARITY_ADDRESS = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
let		RARITY;

describe('Tests', () => {
	let		rarityXPProxy;
    let		rarityXPProxySpender;
    let		user;
	let		nextAdventurer;

    before(async () => {
        await deployments.fixture();
        [user] = await ethers.getSigners();
		RARITY = new ethers.Contract(RARITY_ADDRESS, [
			'function next_summoner() public view returns (uint)',
			'function summon(uint _class) external',
			'function adventure(uint _summoner) external',
			'function setApprovalForAll(address operator, bool _approved) external'
		], user);
		rarityXPProxy = await RarityXPProxy.new()
		rarityXPProxySpender = await RarityXPProxySpender.new(rarityXPProxy.address)
    });

	
	it('should be possible to get the name of the function', async function() {
		const	name = await rarityXPProxy.name();
		await	expect(name).to.be.equal('Rarity XP Proxy');
	})

	it('should not be approvedForAll', async function() {
		const	isApprovedForAll = await rarityXPProxy.isApprovedForAll(user.address);
		await	expect(isApprovedForAll).to.be.false;
	})

	it('should be possible to summon & adventure with a new adventurer', async function() {
		nextAdventurer = Number(await RARITY.next_summoner());
		await	(await RARITY.summon(4)).wait();
		await	(await RARITY.adventure(nextAdventurer)).wait();
	})

	it('should be possible approveForAll', async function() {
		await	(await RARITY.setApprovalForAll(rarityXPProxy.address, true)).wait();
		const	isApprovedForAll = await rarityXPProxy.isApprovedForAll(user.address);
		await	expect(isApprovedForAll).to.be.true;
	})

	it('should not be possible for the spender to spend my XP', async function() {
		await expect(rarityXPProxySpender.spendXP(
			nextAdventurer,
			ethers.utils.parseEther('50'),
			{from: user.address}
		)).to.be.reverted;
	})

	it('should be possible to allow the spender for 100XP', async function() {
		const approveTx = await rarityXPProxy.approve(
			nextAdventurer,
			rarityXPProxySpender.address,
			ethers.utils.parseEther('100'),
			{from: user.address}
		);
		await	expect(approveTx?.receipt?.status).to.be.true;
	})

	it('should be possible for the spender to spend 25XP', async function() {
		const spendTX = await rarityXPProxySpender.spendXP(
			nextAdventurer,
			ethers.utils.parseEther('25'),
			{from: user.address}
		);
		await	expect(spendTX?.receipt?.status).to.be.true;
	})

	it('should be possible for the spender to spend 75XP', async function() {
		const spendTX = await rarityXPProxySpender.spendXP(
			nextAdventurer,
			ethers.utils.parseEther('75'),
			{from: user.address}
		);
		await	expect(spendTX?.receipt?.status).to.be.true;
	})

	it('should not be possible for the spender to spend 1XP', async function() {
		await expect(rarityXPProxySpender.spendXP(
			nextAdventurer,
			ethers.utils.parseEther('1'),
			{from: user.address}
		)).to.be.reverted;
	})

	it('should be possible to allow the spender for 200XP', async function() {
		const approveTx = await rarityXPProxy.approve(
			nextAdventurer,
			rarityXPProxySpender.address,
			ethers.utils.parseEther('200'),
			{from: user.address}
		);
		await	expect(approveTx?.receipt?.status).to.be.true;
	})

	it('should not be possible for the spender to spend 200XP (150 XP left)', async function() {
		await expect(rarityXPProxySpender.spendXP(
			nextAdventurer,
			ethers.utils.parseEther('200'),
			{from: user.address}
		)).to.be.reverted;
	})

	it('should be possible for the spender to spend 150XP', async function() {
		const spendTX = await rarityXPProxySpender.spendXP(
			nextAdventurer,
			ethers.utils.parseEther('150'),
			{from: user.address}
		);
		await	expect(spendTX?.receipt?.status).to.be.true;
	})
});