from brownie import ArtonBattleSystem
from scripts.create_other_artons import ENEMY_ACCOUNT

from scripts.deploy_arton_purchase import display_owners_artons
from scripts.helpful_scripts import get_account

from web3 import Web3


#To receive conclusive information about the tests it is important to run the tests inside each function one by one


def test_can_get_arton():
    abs = ArtonBattleSystem[-1]

    try:
        output = abs.getArtonStruct(0)
        print(output)
    except:
        print("Arton Id out of range")

    try:
        output = abs.getArtonStruct(7)
        print(output)
    except:
        print("Arton Id out of range")


    try:
        output = abs.getArtonStruct(50)
        print(output)
    except:
        print("Arton Id out of range")
    
    try:
        output = abs.getArtonStruct(-50)
        print(output)
    except:
        print("Arton Id out of range")
    
    
def test_can_find_enemy(arton_id, loop_start):
    abs = ArtonBattleSystem[-1]

    try:
        output = abs.findEnemyId(1, loop_start)
        print(output)
    except:
        print("Enemy search failed")


    try:
        output = abs.findEnemyId(7, loop_start)
        print(output)
    except:
        print("Enemy search failed")


    try:
        output = abs.findEnemyId(0, 0)
        print(output)
        assert output != 0
    except:
        print("Enemy search failed")
    
    try:
        output = abs.findEnemyId(-1, 80)
        print(output)
    except:
        print("Enemy search failed")

    try:
        output = abs.findEnemyId(1000, -2)
        print(output)
    except:
        print("Enemy search failed")


def test_can_check_fought(arton_id):
    abs = ArtonBattleSystem[-1]

    try:
     output = abs.checkIfEnemyAlreadyFought(0)
     print(output)
    except:
        print("The owners arton is to be battled")

    try:
     output = abs.checkIfEnemyAlreadyFought(1)
     print(output)
    except:
        print("The owners arton is to be battled")
    
    try:
     output = abs.checkIfEnemyAlreadyFought(6)
     print(output)
    except:
        print("The owners arton is to be battled")
    
    try:
     output = abs.checkIfEnemyAlreadyFought(120)
     print(output)
    except:
        print("The owners arton is to be battled")

    try:
     output = abs.checkIfEnemyAlreadyFought(-5)
     print(output)
    except:
        print("The owners arton is to be battled")

def test_battle(arton_id):
    abs = ArtonBattleSystem[-1]
    
    try:
        outcome = abs.battle(0, {"from": get_account()})
        print(outcome)
    except:
        print("The arton cannot battle")
    
    try:
        outcome = abs.battle(0, {"from": ENEMY_ACCOUNT})
        print(outcome)
    except:
        print("The arton cannot battle")
    
    
    
    try:
        outcome = abs.battle(-1, {"from": get_account()})
        print(outcome)
    except:
        print("The arton cannot battle")
    
    try:
        outcome = abs.battle(2, {"from": get_account()})
        print(outcome)
    except:
        print("The arton cannot battle")

    
    try:
        outcome = abs.battle(6, {"from": ENEMY_ACCOUNT})
        print(outcome)
    except:
        print("The arton cannot battle")

    
    
    try:
        outcome = abs.battle(1000, {"from": get_account()})
        print(outcome)
    except:
        print("The arton cannot battle")

    

def main():
    
    test_battle(arton_id=None)
    display_owners_artons(account=get_account())
    display_owners_artons(account=ENEMY_ACCOUNT)


"""

This is the testing account setup


ENEMY_ACCOUNT
You are the owner of these artons: (4, 5, 6, 7)
///////////////////////////The specs of your Arton at id: 4///////////////////////////
Attack damage: 20
HP: 80
Attack damage: 18
HP: 72
///////////////////////////The specs of your Arton at id: 6///////////////////////////
Attack damage: 59
HP: 236
///////////////////////////The specs of your Arton at id: 7///////////////////////////
Attack damage: 54
HP: 216





DEPLOYER_ACCOUNT

You are the owner of these artons: (0, 1, 2, 3)
///////////////////////////The specs of your Arton at id: 0///////////////////////////
Attack damage: 40
HP: 1
///////////////////////////The specs of your Arton at id: 1///////////////////////////
Attack damage: 56
HP: 224
///////////////////////////The specs of your Arton at id: 2///////////////////////////
Attack damage: 30
HP: 1
///////////////////////////The specs of your Arton at id: 3///////////////////////////
Attack damage: 11
HP: 44


All tests have passed as expected



"""


