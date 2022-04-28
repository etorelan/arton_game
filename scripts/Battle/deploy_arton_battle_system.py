from web3 import Web3
from scripts.create_other_artons import ENEMY_ACCOUNT
from scripts.helpful_scripts import get_account, link
from brownie import ArtonBattleSystem, ArtonPurchase, network
from scripts.deploy_arton_purchase import display_owners_artons

address_art_pur = ArtonPurchase[-1]

def deploy_arton_battle_system(address_art_pur):
    account = get_account()

    abs = ArtonBattleSystem.deploy(address_art_pur, {"from": get_account()})
    print("ArtonBattleSystem has been deployed")
    print(f"The ArtonBattleSystem kovan address: {link[network.show_active()].format(abs)}")

    artonPurchase = ArtonPurchase[-1]
    artonPurchase.setABSAddress(abs, {"from": account})


def main():
    deploy_arton_battle_system(address_art_pur=address_art_pur)
    




    
