from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    deploy_arton_purchase,
    create_2_digit_number,
)
from brownie import ArtonPurchase


def raw_create_arton(eth_value, account):
    account = account if account else get_account()
    if len(ArtonPurchase) <= 0:
        artonPurchase = deploy_arton_purchase()
    else:
        artonPurchase = ArtonPurchase[-1]

    """deposit_tx = artonPurchase.deposit(200000000000000000, {"from": account})
    deposit_tx.wait(1)
    print("Depositing eth")"""

    funding_tx = fund_with_link(
        contract_address=artonPurchase, amount=100000000000000000
    )
    funding_tx.wait(1)

    creating_tx = artonPurchase.rawCreateArton({"from": account, "value": eth_value})
    creating_tx.wait(1)

    print("The random number has been requested")

    return creating_tx


def fullfill_arton_creation(account):
    account = account if account else get_account()
    if len(ArtonPurchase) <= 0:
        artonPurchase = deploy_arton_purchase()
        creating_tx = raw_create_arton(eth_value=200000000000000000, account=account)
        creating_tx.wait(1)
        create_2_digit_number(creating_tx=creating_tx)
    else:
        artonPurchase = ArtonPurchase[-1]
    creating_tx = artonPurchase.fullfillArtonCreation({"from": account})
    creating_tx.wait(1)

    print("Your Arton has been succesfully created")
    attack_damage = creating_tx.events["ArtonSpecs"]["_attackDamage"]
    hp = creating_tx.events["ArtonSpecs"]["_hp"]
    level = creating_tx.events["ArtonSpecs"]["_level"]
    print(f"This is the attack damage of your Arton: {attack_damage}")
    print(f"This is the hp of your Arton: {hp}")
    print(f"This is the level of your Arton: {level}")


def display_owners_artons(account):
    account = account if account else get_account()
    if len(ArtonPurchase) <= 0:
        artonPurchase = deploy_arton_purchase()
    else:
        artonPurchase = ArtonPurchase[-1]

    onwer_id_array = artonPurchase.getOwnersIds(account, {"from": account})
    print("Displaying artons...")
    print(f"You are the owner of these artons: {onwer_id_array}")
    for id in onwer_id_array:
        arton_array = artonPurchase.artons(id, {"from": account})
        print(
            f"///////////////////////////The specs of your Arton at id: {arton_array[4]}///////////////////////////"
        )
        print(f"Attack damage: {arton_array[1]}")
        print(f"HP: {arton_array[2]}")


def main():
    deploy_arton_purchase()

address_art_pur = ArtonPurchase[-1]


