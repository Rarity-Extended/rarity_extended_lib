const {ethers} = require('hardhat');

/**************************************************************************************************
** Hack functions to mint some ERC20
**************************************************************************************************/
async function    mintERC20(address, to, amount, slot = 2) {
    const toBytes32 = (bn) => {
        return ethers.utils.hexlify(ethers.utils.zeroPad(bn.toHexString(), 32));
    };
    const setStorageAt = async (address, index, value) => {
        await ethers.provider.send("hardhat_setStorageAt", [address, index.replace("0x0", "0x"), value]);
        await ethers.provider.send("evm_mine", []); // Just mines to the next block
    };

    const SLOT = slot;
    const index = ethers.utils.solidityKeccak256(
        ["uint", "uint"],
        [to, SLOT]
    );
    await setStorageAt(
        address,
        index.toString(),
        toBytes32(ethers.BigNumber.from(amount)).toString()
    );
}
async function	balanceOf(tokenAddress, user) {
    const abi = ['function balanceOf(uint) external view returns (uint)'];
    const contract = new ethers.Contract(tokenAddress, abi, ethers.provider);
    return (await contract.balanceOf(user)).toString();
}

const	ERC20ABI = [
	'function approve(uint from, uint spender, uint amount) external returns (bool)',
	'function allowance(uint from, uint spender) external view returns (uint)'
];

module.exports = {
    mintERC20,
    balanceOf,
    ERC20ABI
};