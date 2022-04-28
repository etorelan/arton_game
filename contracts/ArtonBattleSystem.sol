//SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;


interface IArtonPurchase {

    struct Arton {
        address owner;
        uint24 attackDamage;
        uint24 hp;
        uint8 level;
        uint256 id;
    }

    function getArton(uint256 _artonId) external view returns (Arton memory);

    function getArtonsArray() external view returns (Arton[] memory);

    function changeArtonHP(uint256 _artonId, uint256 _value) external;
}


contract ArtonBattleSystem {

    uint256 public randNonce = 1;
    ///@dev used in 'randMod(uint256 _modulus)' when determining whether an arton wins or loses

    mapping(uint256 => mapping(uint256 => bool)) enemyFought;
    ///@dev Used to check whether a certain Arton has fought the next generated enemy
    ///@dev to stop an Arton battling the same enemy forever
    

    IArtonPurchase iArtonPurchase;
    constructor(address _artonPurchase) {
        iArtonPurchase = IArtonPurchase(_artonPurchase);
    }


    modifier ownerOf(uint256 _artonId) {
        ///@dev ensures that function caller is the owner of the Arton at '_artonId'
        require(
            iArtonPurchase.getArton(_artonId).owner == msg.sender,
            "Only this arton's owner can call this method"
        );
        _;
    }

    function getArtonStruct(uint256 _id)
        public
        view
        returns (IArtonPurchase.Arton memory)
    {
        ///@dev Returns an arton at a certain '_id'
        IArtonPurchase.Arton memory myArton = iArtonPurchase.getArton(_id);
        return myArton;
    }

    
    function findEnemyId(uint256 _artonId, uint256 _loopStart)
        public
        view
        returns (uint256 _id)
    {
        ///@dev Cycles through the 'artons' array and checks if arton[_artonId] has 
        ///@dev a different level and a different owner than arton[i], if both are  
        ///@dev different the function returns a valid enemy id, if one condition 
        ///@dev isn't met, then i is increased by one. When no Artons can be found
        ///@dev 0 is returned

        require(_loopStart != 0, "Arton 0 can't be battled");

        IArtonPurchase.Arton[] memory artons = iArtonPurchase.getArtonsArray();
        IArtonPurchase.Arton memory myArton = artons[_artonId];

        for (uint256 i = _loopStart; i < artons.length; i++) {

            if (myArton.level == artons[i].level && myArton.owner != artons[i].owner) 
            {
                return artons[i].id;
            }

        }
        return 0;
    }



    function checkIfEnemyAlreadyFought(uint256 _artonId) public view 
        returns (uint)
    {
        ///@dev Calls the 'findEnemyId(uint256 _artonId, uint256 _loopStart)' function 
        ///@dev as long as the found enemy Arton is 'fainted' or already fought
        uint256 enemyId = findEnemyId(_artonId, 1);

        while (enemyFought[_artonId][enemyId] || iArtonPurchase.getArton(enemyId).hp == 1) {
            enemyId = findEnemyId(_artonId, enemyId + 1);
        }
        
        return enemyId;
    }
    


    function randMod(uint256 _modulus) internal returns (uint24) {
        ///@dev creates a pseudo-random number, to determine which Arton wins a fight
        randNonce++; 
        return uint24(uint256(keccak256(abi.encodePacked(block.timestamp, msg.sender, randNonce))) % _modulus);
    }


    function revive(uint256 _artonId) public payable ownerOf(_artonId) {
        ///@dev For a certain price, it sets the arton[_artonId]'s hp to a multiple of its level
        ///@dev making it able to fight and be fought
        require(msg.value > 0.002 ether, "Reviving an Arton costs 0.002 ether");
        require( iArtonPurchase.getArton(_artonId).hp == 1, "You cannot revive a healthy Arton");
        iArtonPurchase.changeArtonHP(_artonId,iArtonPurchase.getArton(_artonId).level * 100);
    }


    function battle(uint256 _artonId) public ownerOf(_artonId) {
        ///@dev Picks an unfought, healthy Arton to fight against a given arton[_artonId]
        ///@dev calls randMod to determine which Artons faints(its hp is set to one, and it is
        ///@dev unable to fight or be fought) based on the attackDamage difference.
        ///@dev Lastly, it labels the enemyArton as fought for the arton[_artonId].
        
        IArtonPurchase.Arton memory myArton = iArtonPurchase.getArton(_artonId);
        IArtonPurchase.Arton memory enemyArton = iArtonPurchase.getArton(checkIfEnemyAlreadyFought(_artonId));

        require(
            enemyArton.hp != 1 && myArton.hp != 1, "Fainted artons cannot battle"
        );


        uint256 winChance = 1;
        ///@dev 'winChance' is set to one, to save a bit of gas.
        ///@dev It is more costly to set a varible from zero to 
        ///@dev a non-zero value, then setting it from non-zero
        ///@dev to non-zero.

        if (myArton.hp > (enemyArton.hp + 15)){
            winChance = 55;
        }else{
             winChance = 40;
        }


        if (randMod(100) <= winChance){
            iArtonPurchase.changeArtonHP(enemyArton.id, 1);
        }else{
            iArtonPurchase.changeArtonHP(myArton.id, 1);
        }

        enemyFought[_artonId][enemyArton.id] = true;

    }
      
}
