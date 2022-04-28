from web3 import Web3
from scripts.deploy_arton_purchase import (
    fullfill_arton_creation,
    display_owners_artons,
)
from brownie import config, accounts

from scripts.helpful_scripts import (
    get_account,
    set_shortRandomNumber,
)
import time

ENEMY_ACCOUNT = accounts.add(config["wallets"]["from_bs"])
account = get_account()




def create_artons(account, eth_amount, first_run):
    first_run = first_run if first_run else False
    set_shortRandomNumber(account, eth_amount)
    if first_run:
        time.sleep(60)
    fullfill_arton_creation(account=account)
    display_owners_artons(account=account)


def main():
    create_artons(account=get_account(), eth_amount=Web3.toWei(0.0015, "ether"))
    
    
