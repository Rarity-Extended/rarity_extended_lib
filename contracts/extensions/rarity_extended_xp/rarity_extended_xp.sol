// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "../../interfaces/IRarity.sol";

contract rarity_xp_proxy {
    IRarity constant _rm = IRarity(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    string constant public name = "Rarity XP Proxy";

    /**
    **  @dev Mapping for the allowances
    **  First param (address) is the address of the owner.
    **  Second param (uint) is the adventurerID
    **  Third param (address) is the address we want to allow to spend XP
    **  Fourth param (uint) is the amount of XP we want to allow to spend
    */
    mapping(address => mapping (uint => mapping (address => uint))) public allowance;

    event Approval(uint indexed adventurer, address indexed operator, uint amount);
    event SpendXP(uint indexed adventurer, uint amount);
    
    /**
    **  @dev Check if the msg.sender has the autorization to act on this adventurer
    **	@param _adventurer: TokenID of the adventurer we want to check
    **/
    function _isApprovedOrOwner(uint _adventurer) internal view returns (bool) {
        return (_rm.getApproved(_adventurer) == msg.sender || _rm.ownerOf(_adventurer) == msg.sender);
    }
    
    /**
    **  @dev Check if this contract has the autorization to act on all the
    **  adventurers of this specific owner
    **	@param _owner: Address to check
    **/
    function isApprovedForAll(address _owner) public view returns (bool) {
        return _rm.isApprovedForAll(_owner, address(this));
    }

    /**
    **  @dev Sets `_amount` as the allowance of `_operator` over the adventurer
    **  `_adventurer`.
    **  @param _adventurer: TokenID of the adventurer we want to set the allowance
    **  @param _operator: Address of the operator we want to set the allowance
    **  @param _amount: Amount of XP we want to set as the allowance
    **
    **  @return a boolean value indicating whether the operation succeeded.
    **  Emits an {Approval} event.
    */
    function approve(uint _adventurer, address _operator, uint _amount) external returns (bool) {
        require(_isApprovedOrOwner(_adventurer));
        address _owner = _rm.ownerOf(_adventurer);
        allowance[_owner][_adventurer][_operator] = _amount;

        emit Approval(_adventurer, _operator, _amount);
        return true;
    }

    /**
    **  @dev Spend `_amount` XP of `_adventurer`. `_amount` is then deducted
    **  from the caller's allowance.
    **  @param _adventurer: TokenID of the adventurer we want to set the allowance
    **  @param _amount: Amount of XP we want to set as the allowance
    **
    **  @return a boolean value indicating whether the operation succeeded.
    **  Emits an {Approval} event.
    */
    function spend_xp(uint _adventurer, uint _amount) external returns (bool) {
        if (_isApprovedOrOwner(_adventurer)) {
            _rm.spend_xp(_adventurer, _amount);
            emit SpendXP(_adventurer, _amount);
            return true;
        }

        address operator = msg.sender;
        address _owner = _rm.ownerOf(_adventurer);
        uint spenderAllowance = allowance[_owner][_adventurer][operator];

        if (spenderAllowance != type(uint).max) {
            uint newAllowance = spenderAllowance - _amount;
            allowance[_owner][_adventurer][operator] = newAllowance;

            emit Approval(_adventurer, operator, _amount);
        }

        _rm.spend_xp(_adventurer, _amount);
        emit SpendXP(_adventurer, _amount);
        return true;
    }

    /**
    **  @dev Check if this contract can spend some XP for a specific adventurer
    **  @param _adventurer: TokenID of the adventurer we want to set the allowance
    **  @param _amount: Amount of XP we want to set as the allowance
    */
    function can_spend_xp(uint _adventurer, uint _amount) external view returns (bool) {
        address operator = msg.sender;
        address _owner = _rm.ownerOf(_adventurer);
        if (!isApprovedForAll(_owner)) {
            return false;
        }
        uint spenderAllowance = allowance[_owner][_adventurer][operator];
        if (spenderAllowance >= _amount) {
            return true;
        }
        return false;
    }
}