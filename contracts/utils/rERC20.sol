// SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "../interfaces/IRarity.sol";
import "../extended.sol";

abstract contract rERC20 is AccessControl, Extended {
    IRarity constant rm = IRarity(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    uint8 public constant decimals = 18;

    string public name;
    string public symbol;
    uint public totalSupply = 0;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor(string memory _name, string memory _symbol) Extended() {
        name = _name;
        symbol = _symbol;
    }

    /*******************************************************************************
	**	@notice
	**		For a contract to be able to mint tokens, it must first be added as a
    **		minter. This is done by calling the `setMinter` function.
    **      The `setMinter` function must be called by the owner of the contract,
    **      aka Extended.
	**	@param _minter The address to add as a Minter.
	*******************************************************************************/
    function setMinter(address _minter) external onlyExtended() {
        _setupRole(MINTER_ROLE, _minter);
    }

    /*******************************************************************************
	**	@notice
	**		For some security reason, the owner should be able to remove a minter.
    **      The `unsetMinter` function must be called by the owner of the contract,
    **      aka Extended.
	**	@param _minter The address to remove as a Minter.
	*******************************************************************************/
    function unsetMinter(address _minter) external onlyExtended() {
        _revokeRole(MINTER_ROLE, _minter);
    }

    mapping(uint => mapping (uint => uint)) public allowance;
    mapping(uint => uint) public balanceOf;

    event Transfer(uint indexed from, uint indexed to, uint amount);
    event Approval(uint indexed from, uint indexed to, uint amount);
    event Burn(uint indexed from, uint amount);
    event Mint(uint indexed to, uint amount);

    function _isApprovedOrOwner(uint _summoner) internal view returns (bool) {
        return rm.getApproved(_summoner) == msg.sender || rm.ownerOf(_summoner) == msg.sender || rm.isApprovedForAll(rm.ownerOf(_summoner), msg.sender);
    }

    function mint(uint to, uint amount) external onlyRole(MINTER_ROLE) {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Mint(to, amount);
    }

    // You can only burn your own tokens
    function burn(uint from, uint amount) external {
        require(_isApprovedOrOwner(from), "!owner");
        totalSupply -= amount;
        balanceOf[from] -= amount;
        emit Burn(from, amount);
    }

    function approve(uint from, uint spender, uint amount) external returns (bool) {
        require(_isApprovedOrOwner(from), "!owner");
        allowance[from][spender] = amount;

        emit Approval(from, spender, amount);
        return true;
    }

    function transfer(uint from, uint to, uint amount) external returns (bool) {
        require(_isApprovedOrOwner(from), "!owner");
        _transferTokens(from, to, amount);
        return true;
    }

    function transferFrom(uint executor, uint from, uint to, uint amount) external returns (bool) {
        require(_isApprovedOrOwner(executor), "!owner");
        uint spender = executor;
        uint spenderAllowance = allowance[from][spender];

        if (spender != from && spenderAllowance != type(uint).max) {
            uint newAllowance = spenderAllowance - amount;
            allowance[from][spender] = newAllowance;

            emit Approval(from, spender, newAllowance);
        }

        _transferTokens(from, to, amount);
        return true;
    }

    function _transferTokens(uint from, uint to, uint amount) internal {
        balanceOf[from] -= amount;
        balanceOf[to] += amount;

        emit Transfer(from, to, amount);
    }
}