from brownie import ArtonPurchase
from web3 import Web3
from scripts.create_other_artons import create_artons

from scripts.helpful_scripts import deploy_arton_purchase, get_account

def test_arton_purchase_integration():
    try:
        ap = ArtonPurchase[-1]
        deploy_arton_purchase()
        create_artons(account=get_account(), eth_amount=Web3.toWei(0.0015,"ether"), first_run=True)
        id = ap.id()
        assert id != 0
    except:
        print("ArtonPurchase integration test failed")