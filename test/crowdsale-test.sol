pragma solidity ^0.5.5;

import "./coin-mint-test.sol";
import "./safemath-test.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";


// Have the BlackSwanCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
// UPDATE THE CONTRACT SIGNATURE TO ADD INHERITANCE
contract BlackSwanCrowdsale is Crowdsale, MintedCrowdsale{ 
    
    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint256 rate,
        address payable wallet,
        BlackSwanCoin token
    ) 
      Crowdsale(rate, wallet, token) 
      public{
        // constructor can stay empty
    }
}


contract BlackSwanCrowdsaleDeployer {
    // Create an `address public` variable called `BlackSwan_token_address`.;
    address public BlackSwan_token_address;
    // Create an `address public` variable called `BlackSwan_crowdsale_address`.
    address public BlackSwan_crowdsale_address;
    // Add the constructor.
    constructor(
        string memory name,
        string memory symbol,
        address payable wallet
    )
    public 
    {
        // Create a new instance of the KaseiCoin contract.
        // Assign the token contract’s address to the `BlackSwan_token_address` variable.
        // Create a new instance of the `BlackSwanCrowdsale` contract
        // Aassign the `BlackSwanCrowdsale` contract’s address to the `BlackSwan_crowdsale_address` variable.
        // Set the `BlackSwanCrowdsale` contract as a minter
        // Have the `BlackSwanCrowdsaleDeployer` renounce its minter role.
        BlackSwan token = new BlackSwanCoin(name, symbol, 0);
        BlackSwan_token_address = address(token);

        BlackSwanCrowdsale BlackSwan_crowdsale=
            new BlackSwanCrowdsale(1, wallet, token);
            BlackSwan_crowdsale_address = address(BlackSwan_crowdsale);

        token.addMinter(BlackSwan_crowdsale_address);
        token.renounceMinter();
        
     
    }
}
