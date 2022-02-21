// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

contract Token
{
    uint public totalSupply = 21000000 * 10 **18; //10^18 means 1 token
    string public name = "Bitcoin";
    string public symbol = "BTC";
    uint public decimal = 18; //10^18 means 1 token

    mapping(address => uint) public balances;
    mapping(address => mapping(address => uint)) public allowance;

    event Transfer(address indexed from, address indexed to, uint amount);
    event Approval(address indexed owner, address indexed spender_on_your_behalf, uint amount);

    constructor()
    {
        balances[msg.sender] = totalSupply;
    }
    
    //BEP-20/ERC-20 token specification
    function balanceOf(address owner) public view returns(uint)
    {
        return balances[owner];
    }

    //BEP-20/ERC-20 token specification
    //simple token transfer
    function transfer(address to, uint amount) public returns(bool)
    {
        require(balanceOf(msg.sender) >= amount, "Low balance");
        balances[msg.sender] -= amount;
        balances[to] += amount;

        emit Transfer(msg.sender, to, amount); //sending events to outside this contract 
        return true;
    }

    //BEP-20/ERC-20 token specification
    function approve(address spender_on_your_behalf, uint amount) public returns(bool)
    {
        allowance[msg.sender][spender_on_your_behalf] = amount;
        emit Approval(msg.sender, spender_on_your_behalf, amount);
        return true;
   }

    //delegated transfer
    //'from' is address where token gets deducted
    //'to' is address where token gets added
    function transferFrom(address from, address to, uint amount) public returns(bool)
    {
        require(balanceOf(from) >= amount, "Low balance");
        require(allowance[from][msg.sender] >= amount, "Exceeded allowed spend limit"); //msg.sender here was pre-approved to send token from 'from' address
        balances[from] -= amount;
        balances[to] += amount;

        allowance[from][msg.sender] -= amount;

        emit Transfer(from, to, amount); //sending events to outside this contract 
        return true;
    }

}
