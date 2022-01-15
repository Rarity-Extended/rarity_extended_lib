async function main() {
    //Compile
    await hre.run("clean");
    await hre.run("compile");

    //Deploy
    this.rarityXPProxy = await ethers.getContractFactory("rarity_xp_proxy");
    this.rarityXPProxy = await this.rarityXPProxy.deploy();
    console.log("Deployed BA to:", this.rarityXPProxy.address);

    //Verify
    await hre.run("verify:verify", {
        address: this.rarityXPProxy.address,
        constructorArguments: [],
    });

}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });