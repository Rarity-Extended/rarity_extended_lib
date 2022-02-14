//SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "../interfaces/IRarity.sol";

/*
    This is a modified version of ERC721, updated to use UINT in ADDRESS. 
    In this case, we attach this NFT to another NFT.
    Note that uint(0) is equivalent to address(0), so holder of the first NFT is burner address and can't access to some functions in contract
*/

interface IrERC721 {
    event Transfer(uint indexed from, uint indexed to, uint256 indexed tokenId);
    event Approval(uint indexed owner, uint indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(uint indexed owner, uint indexed operator, bool approved);
    function balanceOf(uint owner) external view returns (uint256 balance);
    function ownerOf(uint256 tokenId) external view returns (uint owner);
    function transferFrom(
        uint operator,
        uint from,
        uint to,
        uint256 tokenId
    ) external;
    function approve(uint owner, uint to, uint256 tokenId) external;
    function getApproved(uint owner, uint256 tokenId) external view returns (uint operator);
    function setApprovalForAll(uint owner, uint operator, bool _approved) external;
    function isApprovedForAll(uint owner, uint operator) external view returns (bool);
    function permit(
        uint operator,
        uint from,
		uint to,
        uint256 tokenId,
        uint256 deadline,
        bytes calldata signature
    ) external;

    function nonces(uint owner) external view returns (uint256);
    function DOMAIN_SEPARATOR() external view returns (bytes32);
}

abstract contract EIP712 {
    /* solhint-disable var-name-mixedcase */
    // Cache the domain separator as an immutable value, but also store the chain id that it corresponds to, in order to
    // invalidate the cached domain separator if the chain id changes.
    bytes32 private immutable _CACHED_DOMAIN_SEPARATOR;
    uint256 private immutable _CACHED_CHAIN_ID;
    address private immutable _CACHED_THIS;

    bytes32 private immutable _HASHED_NAME;
    bytes32 private immutable _HASHED_VERSION;
    bytes32 private immutable _TYPE_HASH;

    /* solhint-enable var-name-mixedcase */

    /**
     * @dev Initializes the domain separator and parameter caches.
     *
     * The meaning of `name` and `version` is specified in
     * https://eips.ethereum.org/EIPS/eip-712#definition-of-domainseparator[EIP 712]:
     *
     * - `name`: the user readable name of the signing domain, i.e. the name of the DApp or the protocol.
     * - `version`: the current major version of the signing domain.
     *
     * NOTE: These parameters cannot be changed except through a xref:learn::upgrading-smart-contracts.adoc[smart
     * contract upgrade].
     */
    constructor(string memory name, string memory version) {
        bytes32 hashedName = keccak256(bytes(name));
        bytes32 hashedVersion = keccak256(bytes(version));
        bytes32 typeHash = keccak256(
            "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
        );
        _HASHED_NAME = hashedName;
        _HASHED_VERSION = hashedVersion;
        _CACHED_CHAIN_ID = block.chainid;
        _CACHED_DOMAIN_SEPARATOR = _buildDomainSeparator(typeHash, hashedName, hashedVersion);
        _CACHED_THIS = address(this);
        _TYPE_HASH = typeHash;
    }

    /**
     * @dev Returns the domain separator for the current chain.
     */
    function _domainSeparatorV4() internal view returns (bytes32) {
        if (address(this) == _CACHED_THIS && block.chainid == _CACHED_CHAIN_ID) {
            return _CACHED_DOMAIN_SEPARATOR;
        } else {
            return _buildDomainSeparator(_TYPE_HASH, _HASHED_NAME, _HASHED_VERSION);
        }
    }

    function _buildDomainSeparator(
        bytes32 typeHash,
        bytes32 nameHash,
        bytes32 versionHash
    ) private view returns (bytes32) {
        return keccak256(abi.encode(typeHash, nameHash, versionHash, block.chainid, address(this)));
    }

    /**
     * @dev Given an already https://eips.ethereum.org/EIPS/eip-712#definition-of-hashstruct[hashed struct], this
     * function returns the hash of the fully encoded EIP712 message for this domain.
     *
     * This hash can be used together with {ECDSA-recover} to obtain the signer of a message. For example:
     *
     * ```solidity
     * bytes32 digest = _hashTypedDataV4(keccak256(abi.encode(
     *     keccak256("Mail(address to,string contents)"),
     *     mailTo,
     *     keccak256(bytes(mailContents))
     * )));
     * address signer = ECDSA.recover(digest, signature);
     * ```
     */
    function _hashTypedDataV4(bytes32 structHash) internal view virtual returns (bytes32) {
        return ECDSA.toTypedDataHash(_domainSeparatorV4(), structHash);
    }
}


abstract contract rERC721 is IrERC721, EIP712 {
    using Counters for Counters.Counter;
    using Strings for uint256;

    constructor(address _rarityAddr, string memory name) EIP712(name, "1") {
        rm = IRarity(_rarityAddr);
    }

    IRarity public rm;
	bytes32 private immutable _PERMIT_TYPEHASH = keccak256("Permit(uint operator,uint from,uint to,uint tokenId,uint256 nonce,uint256 deadline)");
    mapping(uint256 => uint) private _owners;
    mapping(uint => uint256) private _balances;
    mapping(uint => Counters.Counter) private _nonces;
    mapping(uint256 => mapping(uint => uint)) private _tokenApprovals;
    mapping(uint => mapping(uint => bool)) private _operatorApprovals;

    function balanceOf(uint owner) public view virtual override returns (uint256) {
        require(owner != uint(0), "ERC721: balance query for the zero address");
        return _balances[owner];
    }

    function ownerOf(uint256 tokenId) public view virtual override returns (uint) {
        uint owner = _owners[tokenId];
        require(owner != uint(0), "ERC721: owner query for nonexistent token");
        return owner;
    }

    function _baseURI() internal view virtual returns (string memory) {
        return "";
    }

    function approve(uint from, uint to, uint256 tokenId) public virtual override {
        uint owner = rERC721.ownerOf(tokenId);
        require(_isApprovedOrOwnerOfSummoner(from), "not owner of summoner");

        require(
            from == owner || isApprovedForAll(owner, from),
            "ERC721: approve caller is not owner nor approved for all"
        );

        _approve(from, to, tokenId);
    }

    function getApproved(uint from, uint256 tokenId) public view virtual override returns (uint) {
        require(_exists(tokenId), "ERC721: approved query for nonexistent token");
        return _tokenApprovals[from][tokenId];
    }

    function setApprovalForAll(uint from, uint operator, bool approved) public virtual override {
        require(operator != from, "ERC721: approve to caller");
        require(_isApprovedOrOwnerOfSummoner(from), "not owner of summoner");
        _operatorApprovals[from][operator] = approved;
        emit ApprovalForAll(from, operator, approved);
    }

    function isApprovedForAll(uint owner, uint operator) public view virtual override returns (bool) {
        return _operatorApprovals[owner][operator];
    }

    function transferFrom(
        uint operator,
        uint from,
        uint to,
        uint256 tokenId
    ) public virtual override {
        require(_isApprovedOrOwnerOfSummoner(from), "ERC721: transfer caller is not owner nor approved");
        require(_isApprovedOrOwner(operator, tokenId), "ERC721: transfer operator is not owner nor approved");
        _transfer(from, to, tokenId);
    }


    /**
     * @dev See {IrERC721Permit-permit}.
     */
    function permit(
        uint operator,
        uint from,
		uint to,
        uint256 tokenId,
        uint256 deadline,
        bytes calldata signature
    ) public virtual override {
        require(block.timestamp <= deadline || deadline == 0, "rERC721Permit: expired deadline");
        bytes32 structHash = keccak256(abi.encode(_PERMIT_TYPEHASH, operator, from, to, tokenId, _useNonce(from), deadline));
        bytes32 hash = _hashTypedDataV4(structHash);
        address signer = ECDSA.recover(hash, signature);
        require(rm.getApproved(from) == signer || rm.ownerOf(from) == signer || rm.isApprovedForAll(rm.ownerOf(from), signer), "rERC721Permit: invalid signature");
        _approve(from, operator, tokenId);
    }

    /**
     * @dev See {IrERC721Permit-nonces}.
     */
    function nonces(uint owner) public view virtual override returns (uint256) {
        return _nonces[owner].current();
    }

    /**
     * @dev See {IrERC721Permit-DOMAIN_SEPARATOR}.
     */
    function DOMAIN_SEPARATOR() external view override returns (bytes32) {
        return _domainSeparatorV4();
    }

    /**
     * @dev "Consume a nonce": return the current value and increment.
     *
     * _Available since v4.1._
     */
    function _useNonce(uint owner) internal virtual returns (uint256 current) {
        Counters.Counter storage nonce = _nonces[owner];
        current = nonce.current();
        nonce.increment();
    }

    /**
     * @dev Returns whether `tokenId` exists.
     *
     * Tokens can be managed by their owner or approved accounts via {approve} or {setApprovalForAll}.
     *
     * Tokens start existing when they are minted (`_mint`),
     * and stop existing when they are burned (`_burn`).
     */
    function _exists(uint256 tokenId) internal view virtual returns (bool) {
        return _owners[tokenId] != uint(0);
    }

    /**
     * @dev Returns whether `spender` is allowed to manage `tokenId`.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function _isApprovedOrOwner(uint spender, uint256 tokenId) internal view virtual returns (bool) {
        require(_exists(tokenId), "ERC721: operator query for nonexistent token");
        uint owner = rERC721.ownerOf(tokenId);
        return (spender == owner || getApproved(owner, tokenId) == spender || isApprovedForAll(owner, spender));
    }

    function _isApprovedOrOwnerOfSummoner(uint _summoner) internal view returns (bool) {
        return rm.getApproved(_summoner) == msg.sender || rm.ownerOf(_summoner) == msg.sender || rm.isApprovedForAll(rm.ownerOf(_summoner), msg.sender);
    }

    /**
     * @dev Safely mints `tokenId` and transfers it to `to`.
     *
     * Requirements:
     *
     * - `tokenId` must not exist.
     *
     * Emits a {Transfer} event.
     */
    function _safeMint(uint to, uint256 tokenId) internal virtual {
        _safeMint(to, tokenId, "");
    }

    /**
     * @dev Same as {xref-ERC721-_safeMint-address-uint256-}[`_safeMint`], with an additional `data` parameter.
     */
    function _safeMint(
        uint to,
        uint256 tokenId,
        bytes memory _data
    ) internal virtual {
        _data;
        _mint(to, tokenId);
    }

    /**
     * @dev Mints `tokenId` and transfers it to `to`.
     *
     * WARNING: Usage of this method is discouraged, use {_safeMint} whenever possible
     *
     * Requirements:
     *
     * - `tokenId` must not exist.
     * - `to` cannot be the zero address.
     *
     * Emits a {Transfer} event.
     */
    function _mint(uint to, uint256 tokenId) internal virtual {
        require(to != uint(0), "ERC721: mint to the zero address");
        require(!_exists(tokenId), "ERC721: token already minted");

        _beforeTokenTransfer(uint(0), to, tokenId);

        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(uint(0), to, tokenId);
    }

    /**
     * @dev Destroys `tokenId`.
     * The approval is cleared when the token is burned.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     *
     * Emits a {Transfer} event.
     */
    function _burn(uint256 tokenId) internal virtual {
        uint owner = rERC721.ownerOf(tokenId);

        _beforeTokenTransfer(owner, uint(0), tokenId);

        // Clear approvals
        _approve(owner, uint(0), tokenId);

        _balances[owner] -= 1;
        delete _owners[tokenId];

        emit Transfer(owner, uint(0), tokenId);
    }

    /**
     * @dev Transfers `tokenId` from `from` to `to`.
     *  As opposed to {transferFrom}, this imposes no restrictions on msg.sender.
     *
     * Requirements:
     *
     * - `to` cannot be the zero address.
     * - `tokenId` token must be owned by `from`.
     *
     * Emits a {Transfer} event.
     */
    function _transfer(
        uint from,
        uint to,
        uint256 tokenId
    ) internal virtual {
        require(rERC721.ownerOf(tokenId) == from, "ERC721: transfer of token that is not own");
        require(to != uint(0), "ERC721: transfer to the zero address");

        _beforeTokenTransfer(from, to, tokenId);

        // Clear approvals from the previous owner
        _approve(from, uint(0), tokenId);

        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }

    /**
     * @dev Approve `to` to operate on `tokenId`
     *
     * Emits a {Approval} event.
     */
    function _approve(uint from, uint to, uint256 tokenId) internal virtual {
        _tokenApprovals[from][tokenId] = to;
        emit Approval(rERC721.ownerOf(tokenId), to, tokenId);
    }

    /**
     * @dev Hook that is called before any token transfer. This includes minting
     * and burning.
     *
     * Calling conditions:
     *
     * - When `from` and `to` are both non-zero, ``from``'s `tokenId` will be
     * transferred to `to`.
     * - When `from` is zero, `tokenId` will be minted for `to`.
     * - When `to` is zero, ``from``'s `tokenId` will be burned.
     * - `from` and `to` are never both zero.
     *
     * To learn more about hooks, head to xref:ROOT:extending-contracts.adoc#using-hooks[Using Hooks].
     */
    function _beforeTokenTransfer(
        uint from,
        uint to,
        uint256 tokenId
    ) internal virtual {}
}
