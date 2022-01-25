require("dotenv").config();
const {expect, use} = require('chai');
const {solidity} = require('ethereum-waffle');
const {deployments, ethers} = require('hardhat');

const rarity_extended_proxy_deployer = artifacts.require("rarity_extended_proxy_deployer");
const RarityExtendedName = artifacts.require("rarity_extended_name");

use(solidity);

describe('Tests', () => {
    let		user;
	let		deployer;
    let     proxy_deployer;

    before(async () => {
        await deployments.fixture();
        [deployer, user] = await ethers.getSigners();

		proxy_deployer = await rarity_extended_proxy_deployer.new();
    });
    
	
	it('should be possible to deploy a new contract', async function() {
        let     bytecode = RarityExtendedName._json.bytecode;
        let     nonceBefore = await proxy_deployer.nonce();
		await   proxy_deployer.deploy(bytecode);
        let     nonceAfter = await proxy_deployer.nonce();
		await	expect(Number(nonceBefore)).to.be.equal(Number(nonceAfter) - 1);
	});

});