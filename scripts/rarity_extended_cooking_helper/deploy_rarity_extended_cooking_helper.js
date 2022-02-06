async function main() {
    //Compile
    await hre.run("clean");
    await hre.run("compile");

    //Deploy
    this.Contract = await ethers.getContractFactory("rarity_extended_cooking_helper");
    this.Contract = await this.Contract.deploy('0x6Fa1bee238319Df8eE10677505171EA0278D561b');
    console.log("Deployed to:", this.Contract.address);

    //Verify
    await hre.run("verify:verify", {
        address: this.Contract.address,
        constructorArguments: [],
    });

}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });