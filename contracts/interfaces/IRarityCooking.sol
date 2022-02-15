// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IRarityCooking {
    struct Recipe {
        bool isPaused;
        string name;
        string effect;
        address[] ingredients;
        uint[] quantities;
    }
    function summonerCook() external view returns (uint);
    function getRecipe(address meal) external view returns (string memory, string memory, address[] memory, uint[] memory);
    function cook(address mealAddr, uint chef, uint receiver) external;
    function recipes(address) external view returns (Recipe memory);
    function recipesByIndex(uint) external view returns (Recipe memory);
    function getRecipeByMealName(string memory name) external view returns (Recipe memory);
    function getMealAddressByMealName(string memory name) external view returns (address);
}