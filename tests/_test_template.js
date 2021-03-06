require("dotenv").config();
const {expect, use} = require('chai');
const {solidity} = require('ethereum-waffle');
const {deployments, ethers} = require('hardhat');
const {mintERC20, ERC20ABI} = require('./_test_utils.js');

const YOUR_CONTRACT = artifacts.require("NAME_OF_YOUR_CONTRACT");

use(solidity);

const	RARITY_ADDRESS = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
const   RARITY_GOLD = '0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2';
const	RARITY_ATTRIBUTES = '0xB5F5AF1087A8DA62A23b08C00C6ec9af21F397a1';
const	RARITY_SKILLS = '0x51C0B29A1d84611373BA301706c6B4b72283C80F';
const   RARITY_RAT_SKINS = '0x2A0F1cB17680161cF255348dDFDeE94ea8Ca196A';
let		RARITY;
let		ADVENTURER_ID;
let		TESTED_CONTRACT;

describe('Tests', () => {
    let		user;
	let		deployer;

    before(async () => {
        await deployments.fixture();
        [deployer, user] = await ethers.getSigners();

		/******************************************************************************************
		** Mint and prepare adventurer with lot of intel
		******************************************************************************************/
		RARITY = new ethers.Contract(RARITY_ADDRESS, [
			'function next_summoner() public view returns (uint)',
			'function summon(uint _class) external',
			'function setApprovalForAll(address operator, bool _approved) external',
			'function adventure(uint _summoner) external'
		], user);
		const	ATTRIBUTES = new ethers.Contract(RARITY_ATTRIBUTES, [
			'function point_buy(uint _summoner, uint32 _str, uint32 _dex, uint32 _const, uint32 _int, uint32 _wis, uint32 _cha) external',
		], user);
		const	SKILLS = new ethers.Contract(RARITY_SKILLS, [
			'function set_skills(uint _summoner, uint8[36] memory _skills) external',
		], user);

		ADVENTURER_ID = Number(await RARITY.next_summoner());
		await (await RARITY.summon(1)).wait();
		await (await RARITY.adventure(ADVENTURER_ID)).wait();
		await (await ATTRIBUTES.point_buy(ADVENTURER_ID, 8, 8, 8, 22, 8, 8)).wait();
		const	_skills = Array(36).fill(0);
		_skills[5] = 1
		await (await SKILLS.set_skills(ADVENTURER_ID, _skills)).wait();

        await mintERC20(RARITY_GOLD, ADVENTURER_ID, '80000000000000000000', 2);
		TESTED_CONTRACT = await YOUR_CONTRACT.new();
		GOLD_CONTRACT = new ethers.Contract(RARITY_GOLD, ERC20ABI, user);
    });

	
	it('should be possible to get the name of the function', async function() {
		const	name = await TESTED_CONTRACT.name();
		await	expect(name).to.be.equal('NAME_OF_YOUR_CONTRACT');
	})

	it('Some more test', async function() {
		// ...
	});
});
