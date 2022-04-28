from brownie import ArtonBattleSystem
from web3 import Web3
from scripts.create_other_artons import ENEMY_ACCOUNT
from scripts.deploy_arton_purchase import display_owners_artons
from scripts.helpful_scripts import get_account

abs = ArtonBattleSystem[-1]

def revive_arton(account, arton_id, tx_value):
    abs.revive(arton_id, {"from": account, "value": tx_value})
    display_owners_artons(account=account)


def battle(account, arton_id):
    outcome = abs.checkIfEnemyAlreadyFought(arton_id)
    print(outcome)
    abs.battle(arton_id, {"from": account})
    display_owners_artons(account=account)

def main():
    None



