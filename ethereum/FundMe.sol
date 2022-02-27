// SPDX-License-Identifier: MIT

//accept funding from others (minimum $50) 
pragma solidity ^0.8.2;

//this points to interface.
//interfaces are just blank funtions and don't contains function implementations
//Interfaces compiles down to ABI
//ABI tells Solidity what functions can be called from other contract 
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

//not required in Solidity version 0.8 and above
//import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract FundMe
{
    //using SafeMathChainlink for uint256; //not required in Solidity version 0.8 and above

    address public owner;

    //gets called and immediately executed at very instant this contract gets deployed
    constructor()
    {
        owner = msg.sender;
    }

    mapping(address => uint256) public addressToAmtFunded; //which address contributed how much amount
    address[] public funders;

    function fund() public payable // 'payable' means, this function can be use to pay for things
    {
        //this contract/address would be the owner of whatever coins it has received

        //msg.sender and msg.value are keywords in every contract call and every txn
        //msg.value always comes as wei. 
        //1ETH = 10^18 wei
        //1ETH = 10^9 gwei
        //1gwei = 10^9 wei
        
        uint256 minimumRequiredUSD = 50 * 10 ** 18; //because USD value received from convertWeiToUSD is 10^18 times larger
        uint256 receivedUSD = convertWeiToUSD(msg.value);
        require(receivedUSD >= minimumRequiredUSD, "Require minimum contribution of $50");
        addressToAmtFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256)
    {
        // mention address where the contract that contains the implementation of AggregatorV3Interface is deployed
        // contract address taken from https://docs.chain.link/docs/ethereum-addresses/ for ETH-USD
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version(); //calling function of another contract 
    }

    function getPrice() public view returns(uint256)
    {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (, int256 answer, , , ) = priceFeed.latestRoundData(); //calling function of another contract 
        uint256 decimal = 18 - priceFeed.decimals();
        return uint256(answer) * 10 ** decimal; //making it as 18 decimal
    }

    function convertWeiToUSD(uint256 receivedWei) public view returns(uint256)
    {
        uint256 ETHPrice = getPrice();

        //uint256 receivedUSD = (ETHPrice / 10 ** 18) * (receivedWei / 10 ** 18);
        uint256 receivedUSD = (ETHPrice  * receivedWei) / 10 ** 18; // this should be like above line, 
                                                    //but due to decimal issues only divided by 10^18 here and rest is taken care in minimumRequiredUSD variable.  

        return receivedUSD;
    }

/*
    function withdraw() payable public
    {
        //'this' refers to this particular contract
        //transfering all money from this contract to the owner who deployed this contract
        require(msg.sender == owner, "You are not an owner");
        payable(msg.sender).transfer(address(this).balance);
    }
*/ // use modifier like below to achieve same restriction on this function  


    modifier ownerOnly
    {
        require(msg.sender == owner, "You are not an owner");
        _; //'_' means your functions definitions will be placed here 
    }

    function withdraw() payable ownerOnly public
    {
        //'this' refers to this particular contract
        //transfering all money from this contract to the owner who deployed this contract
        payable(msg.sender).transfer(address(this).balance);

        //reset all funders balance to zero
        for(uint256 index=0; index < funders.length; index++)
        {
            addressToAmtFunded[ funders[index] ] = 0;
        }

        funders = new address[](0); //reset funders array as well
    }

}
