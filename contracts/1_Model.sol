// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract Model {
    event ValuesUpdated(uint256 timestamp, uint256 accuracy, uint256 loss, string application);

    uint256 private _accuracy;
    uint256 private _loss;
    string private _application;

    constructor() {
        _loss = 10000000;
        _accuracy = 0;
        _application = "";
    }

    function setValues(uint256 accuracy, uint256 loss, string memory application) public {
        require(accuracy <= 10000000, "Accuracy value must be less than or equal to 100%");
        require(loss <= 10000000, "Loss value must be less than or equal to 100%");

        _accuracy = accuracy;
        _loss = loss;
        _application = application;
        emit ValuesUpdated(block.timestamp, _accuracy, _loss, _application);
    }

    function getAccuracy() public view returns (uint256) {
        return _accuracy;
    }

    function getLoss() public view returns (uint256) {
        return _loss;
    }

    function getApplication() public view returns (string memory) {
        return _application;
    }
}
