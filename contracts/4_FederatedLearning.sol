// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract FederatedLearning {
    
    address[] public network; // Array to store all registered wallet addresses
    mapping(address => bool) public isRegistered; // Mapping to keep track of registered wallet addresses
    mapping(address => bool) public hasConsented; // Mapping to keep track of participating clients
    mapping(address => bool) public consentReceived; // Mapping to keep track of whether client has informed their consent or not
    mapping(address => string) public ipAddresses; // Mapping to store IP addresses of clients
    
    address public initiator; // Address of the client initiating the federated learning round
    
    event ClientRegistered(address indexed client);
    event FederatedLearningRoundInitiated(address indexed initiator);
    event ClientConsented(address indexed client, bool consent);
    event FederatedLearningRoundCompleted();
    
    modifier onlyRegistered() {
        require(isRegistered[msg.sender], "Client is not registered.");
        _;
    }
    
    modifier onlyInitiator() {
        require(msg.sender == initiator, "Only the initiator can perform this action.");
        _;
    }
    
    function register() public {
        require(!isRegistered[msg.sender], "Client is already registered.");
        network.push(msg.sender);
        isRegistered[msg.sender] = true;
        emit ClientRegistered(msg.sender);
    }
    
    function initiate(string memory ipAddress) public onlyRegistered {
        require(initiator == address(0), "Federated learning round is already initiated.");
        initiator = msg.sender;
        ipAddresses[msg.sender] = ipAddress;
        emit FederatedLearningRoundInitiated(msg.sender);
    }
    
    function participate(bool consent) public onlyRegistered {
        require(initiator != address(0), "Federated learning round is not initiated.");
        hasConsented[msg.sender] = consent;
        consentReceived[msg.sender] = true;
        emit ClientConsented(msg.sender, consent);
    }
    
    function getInitiatorIP(address client) public view onlyRegistered returns (string memory) {
        require(initiator != address(0), "Federated learning round is not initiated.");
        require(hasConsented[client], "Client has not yet consented to participate.");
        require(hasConsented[client] == false, "Client has not consented to participate.");
        return ipAddresses[initiator];
    }
    
    function cleanup() public onlyInitiator {
        require(allConsentsReceived(), "Not all clients have given their consent yet.");
        for (uint i = 0; i < network.length; i++) {
            delete isRegistered[network[i]];
            delete hasConsented[network[i]];
            delete consentReceived[network[i]];
            delete ipAddresses[network[i]];
        }
        delete network;
        delete initiator;
        emit FederatedLearningRoundCompleted();
    }
    
    function allConsentsReceived() public view returns (bool) {
        for (uint i = 0; i < network.length; i++) {
            if (!consentReceived[network[i]]) {
                return false;
            }
        }
        return true;
    }
}
