// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract HashStorageLocal {
    event HashUpdated(uint256 timestamp, string hashValue, string application);

    string public _hashValue;
    string private _application;

    function storeHash(string memory hash, string memory application) public {
        _hashValue = hash;
        _application = application;
        emit HashUpdated(block.timestamp, _hashValue, _application);
    }

    function getHash() public view returns (string memory) {
        return _hashValue;
    }

    function getApplication() public view returns (string memory) {
        return _application;
    }
}