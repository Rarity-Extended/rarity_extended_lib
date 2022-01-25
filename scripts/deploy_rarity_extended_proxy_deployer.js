async function main() {
    //Compile
    await hre.run("clean");
    await hre.run("compile");

    //Deploy
    this.Contract = await ethers.getContractFactory("rarity_extended_proxy_deployer");
    this.Contract = await this.Contract.deploy();
    console.log("Deployed to:", this.Contract.address);

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