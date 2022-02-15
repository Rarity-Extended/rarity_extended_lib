const { expect } = require("chai");
const { rarityManifestedAddr } = require("../registry.json");

describe("Basic set", function () {

    before(async function () {
        this.timeout(6000000000);

        [this.user, this.anotherUser, ...this.others] = await ethers.getSigners();

        this.basicSetPrice = ethers.utils.parseUnits("1");

        //Deploy
        this.Contract = await ethers.getContractFactory("rarity_extended_basic_set");
        this.contract = await this.Contract.deploy(rarityManifestedAddr, this.basicSetPrice);
        await this.contract.deployed();

        //Mint summoner
        this.rarity = new ethers.Contract(rarityManifestedAddr, [
            'function approve(address to, uint256 tokenId) external',
            'function summon(uint _class) external',
            'function next_summoner() external view returns(uint)',
        ], this.anotherUser);

        this.summoner = await this.rarity.next_summoner();
        await this.rarity.connect(this.anotherUser).summon(1);
    });

    it("Should deploy a new set, successfully...", async function () {
        this.timeout(6000000000);

        let setName = "Wonderful basic set";
        let head = 8; // sorcerer hat
        let body = 3; // slain warrior armor
        let hand = 10; // metal glove
        let foot = 11; // hero boots
        let weapon = 3; // andre sword

        await this.contract.deployNewSet(
            setName,
            head,
            body,
            hand,
            foot,
            weapon
        );

        await expect(this.contract.connect(this.anotherUser).deployNewSet(
            setName,
            head,
            body,
            hand,
            foot,
            weapon
        )).to.be.revertedWith("!owner");

        let set = await this.contract.sets(1);
        expect(set.setName).equal(setName);
        expect(set.head).equal(head);
        expect(set.body).equal(body); hand
        expect(set.hand).equal(hand);
        expect(set.foot).equal(foot);
        expect(set.weapon).equal(weapon);

    });

    it("Should buy a set, successfully...", async function () {
        this.timeout(6000000000);

        await this.contract.connect(this.anotherUser).buySet(1, this.summoner, { value: this.basicSetPrice });
        await expect(this.contract.connect(this.anotherUser).buySet(1, this.summoner, { value: 0 })).to.be.revertedWith("!basicSetPrice");
        await expect(this.contract.connect(this.anotherUser).buySet(0, this.summoner, { value: this.basicSetPrice })).to.be.revertedWith("!setIndex");
        await expect(this.contract.connect(this.anotherUser).buySet(69, this.summoner, { value: this.basicSetPrice })).to.be.revertedWith("!emptySet");

        let balanceInContract = await ethers.provider.getBalance(this.contract.address);
        expect(balanceInContract).equal(this.basicSetPrice);
    });

    it("Should get money, successfully...", async function () {
        this.timeout(6000000000);

        let balanceInExtendedBefore = await ethers.provider.getBalance(this.user.address);
        let balanceInContractBefore = await ethers.provider.getBalance(this.contract.address);
        await this.contract.getMoney();
        let balanceInExtendedAfter = await ethers.provider.getBalance(this.user.address);
        let balanceInContractAfter = await ethers.provider.getBalance(this.contract.address);

        await expect(this.contract.connect(this.anotherUser).getMoney()).to.be.revertedWith("!owner");

        expect(balanceInContractAfter).equal(0);
        expect(Number(balanceInContractAfter)).lessThan(Number(balanceInContractBefore));
        expect(Number(balanceInExtendedAfter)).greaterThan(Number(balanceInExtendedBefore));
    });

});