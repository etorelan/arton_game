from brownie import ArtonBattleSystem, ArtonPurchase
from web3 import Web3
from scripts.Battle import deploy_arton_battle_system
from scripts.Battle.arton_actions import battle, revive_arton
from scripts.helpful_scripts import get_account

def test_arton_battle_system_integration(_artonId, _account):
    try:
        deploy_arton_battle_system(address_art_pur=ArtonPurchase[-1])
        battle(_account, _artonId)
        test_arton_arr = abs.getArtonStruct(_artonId)
        if test_arton_arr[2] == 0:
            revive_arton(account=get_account(), arton_id= _artonId, tx_value=Web3.toWei(0.0025,"ether"))
    except:
        print("ArtonBattleSystem integration test has failed")
