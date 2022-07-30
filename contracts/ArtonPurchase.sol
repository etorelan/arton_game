//SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

/// @author etorelan
/// @notice This contract enables the creation of randomly generated creatures named Artons
/**  
*    @dev This contract is 1/2 of the Arton contract saga, to get the address of the 2/2
*    ArtonBattleSystem read the 'artonBattleSystemAddress' variable
*/


import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ArtonPurchase is VRFConsumerBase, Ownable {
    

    /**
    *@dev ↓ These variables (vrfCoordinator, linkToken, keyHash, fee) 
    *       are needed for the Chainlink VRF to receive a random number
    *       for further reading it is recommended to check the Chainlink VRF 
    *       github 
    *       https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/VRFConsumerBase.sol
    *       
    */
    address public vrfCoordinator;
    address public linkToken;
    bytes32 internal keyHash;  
    uint256 internal fee;  

    address public artonBattleSystemAddress;
    /// @dev The address of the currently deployed ArtonBattleSystem contract

    uint8 public lastRandomNumber; 
    ///@dev The previous value of the 'randomResult' variable 

    uint8 public shortRandomResult;
    /**@dev A two-digit random number generated from 'randomResult'
    *  @dev used in the 'fulfillArtonCreation()* function 
    */


    uint256 public id; 
    ///@dev  The identification number of the next created arton, also the current number of Artons

    uint256 public randomResult; 
    /// @dev The random number delivered by the Chainlink VRF
    

    mapping(address => uint256) ownerArtonCount; 
    /**@dev Assigning a user their Artons,
    *   @dev neeed to get all user's Artons in 'getOwnersIds(address _owner)'
    */

    mapping(address => uint8) public requestedLevel;
    /**@dev Assinging a user the requested level of their Arton 
    *   @dev based on msg.value in 'rawCreateArton()' 
    */

    Arton[] public artons; /// @dev Array of all artons created

    

    event RequestedRandomness(bytes32 requestId); 
    /**@dev This event gets emitted during rawCreateArton() 
    *   @dev and is required to receive a random number from 
    *   @dev the Chainlink VRF
    *   @dev 
    */ 
    //↑ 
    event LevelRequested(uint8 level);
    /**@dev Event emitting the artons's level needed to assing 
    *   @dev 'shortRandomNumber' variable and to create an Arton
    */

    modifier artonsAvailable(){
        require(id <= 100, "All artons have been taken");
        _;
    }

    modifier onlyABS() {
        require(
            msg.sender == artonBattleSystemAddress,
            "Only this arton's owner can call this method"
        );
        _;
    }

    modifier ownerOf(uint256 _artonId) {
        require(
            artons[_artonId].owner == msg.sender,
            "Only this arton's owner can call this method"
        );
        _;
    }

    
    ///@dev functions used in the ArtonBattleSystem contract
    function getArton(uint256 _artonId) external view returns (Arton memory) {
        return artons[_artonId];
    }

    function getArtonsArray() external view returns (Arton[] memory) {
        return artons;
    }

    function setABSAddress(address _abs) external onlyOwner{
        artonBattleSystemAddress = _abs;
    }

    function changeArtonHP(uint _artonId, uint _value) external onlyABS{
        artons[_artonId].hp = uint24(_value);
    }
    
    

    constructor(
        address _vrfCoordinator, ///@dev address of the vrf_coordinator on a certain network
        address _linkToken, ///@dev address of the LINK token on a certain network
        bytes32 _keyHash, ///@dev keyhash used by the Chainlink VRF on a certain network
        uint256 _fee ///@dev required fee to receive a random number on a certain network
    ) VRFConsumerBase(_vrfCoordinator, _linkToken) {
        vrfCoordinator = _vrfCoordinator;
        linkToken = _linkToken;
        keyHash = _keyHash;
        fee = _fee;
    }

    
    ///@dev function called by the Chainlink VRF to set randomResult 
    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        randomResult = randomness;
    }
       

    struct Arton {
        address owner;
        uint24 attackDamage;
        uint24 hp;
        uint8 level;
        uint256 id;
    }
    
    enum ARTON_CREATION_STATE {
        INVALID,
        VALID
    }

    ARTON_CREATION_STATE arton_creation_state = ARTON_CREATION_STATE.INVALID;

      /**@dev ↓The most useful event needed in several scripts↓ 
    *   @dev ↓to provide information about the Arton at hand↓
    */    
    event ArtonSpecs(
        address _owner,
        uint24 _attackDamage,
        uint24 _hp,
        uint8 _level,
        uint256 _id
    );

    

    function rawCreateArton() public payable artonsAvailable{
        require(
            (msg.value) >= 0.001 ether,
            "To create an arton deposit 0.1 ether or more"
        );
        ///@dev The Arton creation process starts with this function and ends with 'fullfillArtonCreation()'
        ///@dev it is vital that this function is run only once before 'fullfillArtonCreation()' is called
        ///@dev because it is Needed to stop a person paying for several Artons and creating only one
        require(requestedLevel[msg.sender] == 0, "You already have an Arton in the making, call fullfillArtonCreation");

        if (msg.value < 0.002 ether) {
            requestedLevel[msg.sender] = 1;
        } else if (
            (0.002 ether  <= msg.value) &&
            (msg.value < 0.003 ether)
        ) {
            requestedLevel[msg.sender] = 2;
        } else {
            requestedLevel[msg.sender] = 3;
        }

        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
        emit LevelRequested(requestedLevel[msg.sender]);
    }

    

    function setRandomNumber(uint8 _number) public onlyOwner {
        ///@dev Called by the contract's owner to assign a two-digit number
        ///@dev  as the attackDamage of an Arton from which the hp is calculated 
        shortRandomResult = _number;
        arton_creation_state = ARTON_CREATION_STATE.VALID;
    }

    

    function fullfillArtonCreation() public artonsAvailable{
        require(
            requestedLevel[msg.sender] != 0,
            "You must first call rawCreateArton() to call fullfillArtonCreation()"
        );

        require(
            arton_creation_state == ARTON_CREATION_STATE.VALID,
            "The random number is loading, try again in a minute"
        );

        require(
            (shortRandomResult != 0 && lastRandomNumber != shortRandomResult),
            "The random number is loading, try again in a minute"
        );

        lastRandomNumber = shortRandomResult;

        Arton memory myArton = Arton(
            msg.sender,
            uint24(shortRandomResult),
            uint24(shortRandomResult) * 4,
            requestedLevel[msg.sender],
            id
        );

        artons.push(myArton);
        ownerArtonCount[msg.sender]++;
        emit ArtonSpecs(
            msg.sender,
            myArton.attackDamage,
            myArton.hp,
            myArton.level,
            id
        );
        id++;
        requestedLevel[msg.sender] = 0;
        arton_creation_state = ARTON_CREATION_STATE.INVALID;
    }


    
    function getOwnersIds(address _owner)
        external
        view
        returns (uint256[] memory)
    {
        ///@dev cycles through the entire 'artons' array to find
        ///@dev all Artons belonging to '_owner'. This function
        ///@dev is the reason why the 'artonsAvailable' modifier
        ///@dev exists, otherwise it would be possible to surpass
        ///@dev the gas limit, consume gas and still return nothing 
        uint256[] memory result = new uint256[](ownerArtonCount[_owner]);
        uint256 counter = 0;
        for (uint256 i = 0; i < artons.length; i++) {
            if (artons[i].owner == _owner) {
                result[counter] = i;
                counter++;
            }
        }
        return result;
    }

    function withdrawLink() external onlyOwner {
        ///@dev Transfers this contract's LINK balance to the owner
        payable(msg.sender).transfer(LINK.balanceOf(address(this)));
    }
}
