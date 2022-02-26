// SPDX-License-Identifier: MIT

//deploy a contract from another contract, and interact with it, and call its functions
pragma solidity ^0.8.2;

import "./SimpleStorage.sol";

contract StorageFactory
//contract StorageFactory is SimpleStorage //Inherit all functions and variables from SimpleStorage
{
    SimpleStorage[] public arrayOfContracts; //store deployed contracts

    function createSimpleStorageContract() public
    {
        //created a new SimpleStorage contract from StorageFactory contract
        SimpleStorage newcontractaddress = new SimpleStorage();
        arrayOfContracts.push(newcontractaddress); //push new deployed contract in array
    }

    function sfStore(uint256 contractindex, uint256 num) public
    {
        SimpleStorage contractaddress = SimpleStorage(address(arrayOfContracts[contractindex]));//get address of contract using 'address'
        contractaddress.store(num); //calling SimpleStorage's contract function
    }

    function sfRetrieve(uint256 contractindex) public view returns(uint256)
    {
        SimpleStorage contractaddress = SimpleStorage(address(arrayOfContracts[contractindex]));//get address of contract using 'address'
        return contractaddress.retrieve(); //calling SimpleStorage's contract function
    }

}