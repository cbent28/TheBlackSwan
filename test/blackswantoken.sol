pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";


contract Certificate is ERC721Full {
    constructor() public ERC721Full("Certificate", "CERT") {}
    using SafeMath for uint;

    address payable owner = msg.sender;
    string public symbol = "BSET";
    uint public exchange_rate = 100;

    function mint(address student, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newCertificateId = totalSupply();
        _mint(student, newCertificateId);
        _setTokenURI(newCertificateId, tokenURI);

        return newCertificateId;
    }

    mapping(address => uint) balances;

    function balance() public view returns(uint) {
        return balances[msg.sender];
    }
}
