## RarityExtended Care
Rarity Extended Care is a smartContract that will be used with RarityExtended to provide a more advanced and secure way to manage all of your adventurers in one call.  
This can be see as an extension of Rarity to be able to perfom batch actions, including :
- **Performing the daily Adventure**
- **Performing the daily Cellar**
- **Level upping your adventurers**
- **Claiming gold for your adventurers**

All of them can be done individually, but it is recommended to use the batch action, aka `care_of`.


#### Usage
In order to be able to use this contract with your summoners, you must, first, call the `setApprovalForAll` function of the `Rarity` contract.  
Here is the function :  
```js
function setApprovalForAll(address operator, bool approved) public virtual override {
    require(operator != msg.sender, "ERC721: approve to caller");

    _operatorApprovals[msg.sender][operator] = approved;
    emit ApprovalForAll(msg.sender, operator, approved);
}
```

This function is not very safe and must be used with caution : It allows the `Operator` to perform approval in your name for all your summoners. We are using this function to allow the `Extended Care` to perform the daily actions of the `Rarity` contract for you, saving gas and preventing multiple transaction. This contract doesn't have the possibility to move your funds or summoner.

Once you have performed the setApprovalForAll, you can use the `care_of` function to perform the batch actions.
```js
function care_of(uint[] memory _summoners, bool[4] memory _whatToDo, uint _threshold_cellar) external
```

The `care_of` function takes 3 parameters :
- `_summoners` : The array of summoners to perform the batch actions.
- `_whatToDo` : The array of boolean that represent the actions to perform. The order is : `[daily_adventure, daily_cellar, level_up, claim_gold]`.
- `_threshold_cellar` : The threshold to perform the cellar.

For example, if you want to perform the daily adventure + the daily cellar for all your summoners, you can do :
```js
care_of([12345, 23456, 65432], [true, true, false, false], 1)
```

**[Deployed here](https://ftmscan.com/address/0xc066618F5c84D2eB002b99b020364D4CDDE6245D)**