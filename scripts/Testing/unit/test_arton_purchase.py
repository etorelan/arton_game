from brownie import ArtonPurchase
from web3 import Web3
from scripts.create_other_artons import ENEMY_ACCOUNT

from scripts.deploy_arton_purchase import display_owners_artons, fullfill_arton_creation, raw_create_arton
from scripts.helpful_scripts import get_account, fund_with_link, set_shortRandomNumber

import time

ap = ArtonPurchase[-1]

def test_get_arton(arton_id):
    try:
        arr = ap.getArton(3)
        print(arr)
    except:
        print("Cannot call getArton function in ArtonPurchase.sol")



def test_get_artons_array():
    try:
        arr = ap.getArtonsArray()
        print(arr)
    except:
        print("Cannot call getArtonsArray function in ArtonPurchase.sol")



def test_set_abs_address():
    try:
        ap.setABSAddress('0x271682DEB8C4E0901D1a1550aD2e64D568E69909',{"from": ENEMY_ACCOUNT})
    except:
        print("Address of the ArtonBattleSystem cannot be set from anyone apart the owner")

    try:
        ap.setABSAddress('0x271682DEB8C4E0901D1a1550aD2e64D568E69909')
    except:
        print("Address of the ArtonBattleSystem cannot be set from anyone apart the owner")



def test_change_arton_hp():
    try:
        ap.changeArtonHP(0, 5, {"from": get_account()})
    except:
        print("Address of the ArtonBattleSystem cannot be set from anyone apart the owner") 


    try:
        ap.changeArtonHP(0, 5)
    except:
        print("Address of the ArtonBattleSystem cannot be set from anyone apart the owner") 

    
    try:
        ap.changeArtonHP(0, 5, {"from": ENEMY_ACCOUNT})
    except:
        print("Address of the ArtonBattleSystem cannot be set from anyone apart the owner") 



def test_raw_create_arton():
    try:
        creating_tx = raw_create_arton(eth_value=Web3.toWei(0.0015, "ether"), account=get_account())
        creating_tx.wait(1)
        level = creating_tx.events["LevelRequested"]["level"]
        time.sleep(60)
        rand = ap.randomResult()
        assert rand != 0
        assert level == 1
    except:
        print("rawCreateArton does not set randomNumber or provide the correct level")


    try:
        
        creating_tx = raw_create_arton(eth_value=Web3.toWei(0.0025, "ether"), account=get_account())
        creating_tx.wait(1)
        level = creating_tx.events["LevelRequested"]["level"]
        time.sleep(60)
        rand = ap.randomResult()
        assert rand != 0
        assert level == 2
    except:
        print("rawCreateArton does not set randomNumber or provide the correct level")



    try:
        creating_tx = raw_create_arton(eth_value=Web3.toWei(0.0035, "ether"), account=get_account())
        creating_tx.wait(1)
        level = creating_tx.events["LevelRequested"]["level"]
        time.sleep(60)
        rand = ap.randomResult()
        assert rand != 0
        assert level == 3
    except:
        print("rawCreateArton does not set randomNumber or provide the correct level")



def test_set_random_number():
    try:
        ap.setRandomNumber(8)
    except:
        print("setRandomNumber was not succesful")


    try:
        ap.setRandomNumber(87, {"from": get_account()})
    except:
        print("setRandomNumber was not succesful")

    
    try:
        ap.setRandomNumber(87, {"from": ENEMY_ACCOUNT})
    except:
        print("setRandomNumber was not succesful")



def test_fulfill_arton_creation():

        "rawCreateArton did not run, therefore this test ↓ should have failed"
        try:
            fullfill_arton_creation(account=get_account())
        except:
            print("fulfillArtonCreation was not succesful")

        
        try:
            set_shortRandomNumber(account=get_account(), eth_amount=Web3.toWei(0.0015,"ether"))
            fullfill_arton_creation(account=get_account())
        except:
            print("fulfillArtonCreation was not succesful")





def main():
    None
    