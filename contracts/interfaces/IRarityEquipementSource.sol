// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IEquipementSource {
    function ownerOf(uint256 tokenId) external view returns (address owner);
    function getApproved(uint256 tokenId) external view returns (address operator);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function isValid(uint _base_type, uint _item_type) external pure returns (bool);
    function items(uint tokenID) external view returns (uint8 base_type, uint8 item_type, uint32 crafted, uint256 crafter);
    function supportsInterface(bytes4 interfaceID) external view returns (bool);
}