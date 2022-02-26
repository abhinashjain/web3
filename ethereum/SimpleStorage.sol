// SPDX-License-Identifier: MIT

pragma solidity ^0.8.2;

contract SimpleStorage
{
    uint256 number; //implicitly iniatialized to zero
    struct people
    {
        uint256 num;
        string name;
    }

    //people public person = people(1, "hello");
    people[] public person; //dynamic array
    mapping(string => uint256) public map;

    function add(uint256 num, string memory str) public
    {
        person.push(people(num, str));
        map[str] = num;
    }

    function store(uint256 num) public
    {
        number = num;
    }

    function retrieve() public view returns(uint256)
    {
        return number;
    }

}


