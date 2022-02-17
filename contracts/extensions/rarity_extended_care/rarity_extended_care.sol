// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "../../interfaces/IRarity.sol";
import "../../interfaces/IRarityGold.sol";
import "../../interfaces/IRarityTheCellar.sol";

contract rarity_extended_care {
    IRarity constant _rm = IRarity(0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb);
    IRarityGold constant _gold = IRarityGold(0x2069B76Afe6b734Fb65D1d099E7ec64ee9CC76B2);
    IRarityTheCellar constant _cellar = IRarityTheCellar(0x2A0F1cB17680161cF255348dDFDeE94ea8Ca196A);
    string constant public name = "Rarity Extended Care";
    mapping(address => mapping(uint => bool)) public allowance;

    /**
    **  @dev Perform an adventure for an array of summoners
    **  @param _summoners array of tokenID to use
    */
    function adventure(uint[] memory _summoners) external {
        for (uint256 i = 0; i < _summoners.length; i++) {
            require(_isApprovedOrOwner(_summoners[i]));
            if (block.timestamp > _rm.adventurers_log(_summoners[i])) {
                _rm.adventure(_summoners[i]);
            }
        }
    }
    
    /**
    **  @dev Send a group of adventurer in the cellar
    **  @param _summoners array of tokenID to use
    **  @param _threshold minimum amount of crafting materials expected
    */
    function adventure_cellar(uint[] memory _summoners, uint _threshold) external {
        for (uint256 i = 0; i < _summoners.length; i++) {
            require(_isApprovedOrOwner(_summoners[i]));
            if (block.timestamp > _cellar.adventurers_log(_summoners[i])) {
                uint _reward = _cellar.scout(_summoners[i]);
                if (_reward >= _threshold) {
                    helper_isApprovedOrApprove(_summoners[i]);
                    _cellar.adventure(_summoners[i]);
                }
            }
        }
    }
    
    /**
    **  @dev Level up an array of summoners
    **  @param _summoners array of tokenID to use
    */
    function level_up(uint[] memory _summoners) external {
        for (uint256 i = 0; i < _summoners.length; i++) {
            require(_isApprovedOrOwner(_summoners[i]));
            uint _level = _rm.level(_summoners[i]);
            uint _xp_required = helper_xp_required(_level);
            uint _xp_available = _rm.xp(_summoners[i]);
            if (_xp_available >= _xp_required) {
                _rm.level_up(_summoners[i]);
            }
        }
    }
    
    /**
    **  @dev Claim gold for an array of summoners
    **  @param _summoners array of tokenID to use
    */
    function claim_gold(uint[] memory _summoners) external {
        for (uint256 i = 0; i < _summoners.length; i++) {
            require(_isApprovedOrOwner(_summoners[i]));
            helper_isApprovedOrApprove(_summoners[i]);
            uint _claimable = _gold.claimable(_summoners[i]);
            if (_claimable > 0) {
                _gold.claim(_summoners[i]);
            }
        }
    }
    
    /**
    **  @dev For an array of summoners, try to adventure, then try
    **  to level up, then try to claim gold for each of them.
    **  @param _summoners array of tokenID to use
    **  @param _whatToDo array of bool for what to do [adventure, cellar, levelup, gold]
    **  @param _threshold_cellar minimum amount of crafting materials expected
    */
    function care_of(uint[] memory _summoners, bool[4] memory _whatToDo, uint _threshold_cellar) external {
        for (uint256 i = 0; i < _summoners.length; i++) {
            require(_isApprovedOrOwner(_summoners[i]));
            helper_isApprovedOrApprove(_summoners[i]);
            if (_whatToDo[0]) {
                if (block.timestamp > _rm.adventurers_log(_summoners[i])) {
                    _rm.adventure(_summoners[i]);
                }
            }
            if (_whatToDo[1]) {
                if (block.timestamp > _cellar.adventurers_log(_summoners[i])) {
                    uint _reward = _cellar.scout(_summoners[i]);
                    if (_reward >= _threshold_cellar) {
                        _cellar.adventure(_summoners[i]);
                    }
                }
            }
            if (_whatToDo[2]) {
                uint _level = _rm.level(_summoners[i]);
                uint _xp_required = helper_xp_required(_level);
                uint _xp_available = _rm.xp(_summoners[i]);
                if (_xp_available >= _xp_required) {
                    _rm.level_up(_summoners[i]);
                }
            }
            if (_whatToDo[3]) {
                uint _claimable = _gold.claimable(_summoners[i]);
                if (_claimable > 0) {
                    _gold.claim(_summoners[i]);
                }
            }
        }
    }

    /**
    **  @dev Allow an address to use some summoners
    **  @param _summoners array of tokenID to use
    **  @param _operator address allowed to use the summoners
    **  @param _appoved approved or not
    */
    function setAllowance(uint[] memory _summoners, address _operator, bool _appoved) external {
        for (uint256 i = 0; i < _summoners.length; i++) {
            require(_isApprovedOrOwner(_summoners[i]));
            allowance[_operator][_summoners[i]] = _appoved;
        }
    }

    /**
    **  @dev Compute the xp required to level up
    **	@param curent_level: level of the summoner
    **/
    function helper_xp_required(uint curent_level) public pure returns (uint xp_to_next_level) {
        xp_to_next_level = curent_level * (curent_level + 1) * 500e18;
    }
    
    /**
    **  @dev Check if the summoner is approved for this contract as getApprovedForAll is
    **  not used for gold & cellar.
    **	@param _adventurer: TokenID of the adventurer we want to check
    **/
    function helper_isApprovedOrApprove(uint _summoner) internal {
        address _approved = _rm.getApproved(_summoner);
        if (_approved != address(this)) {
            _rm.approve(address(this), _summoner);
        }
    }

    /**
    **  @dev Check if the msg.sender has the autorization to act on this adventurer
    **	@param _adventurer: TokenID of the adventurer we want to check
    **/
    function _isApprovedOrOwner(uint _summoner) internal view returns (bool) {
        return (
            _rm.getApproved(_summoner) == msg.sender ||
            _rm.ownerOf(_summoner) == msg.sender ||
            allowance[msg.sender][_summoner] == true
        );
    }
}
