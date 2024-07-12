// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentVerification {
    mapping(string => bool) private documents;
    
    event DocumentAdded(string indexed documentHash);
    
    function addDocument(string memory documentHash) public {
        require(!documents[documentHash], "Document already exists");
        documents[documentHash] = true;
        emit DocumentAdded(documentHash);
    }
    
    function verifyDocument(string memory documentHash) public view returns (bool) {
        return documents[documentHash];
    }
}