import random
from brownie import (
    accounts,
    network,
    config,
    Contract,
    LinkToken,
    ArtonPurchase,
)


link = {"kovan" : "https://kovan.etherscan.io/address/{}", "bsc-test" : "https://testnet.bscscan.com/address/{}"}



FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


contract_to_mock = {"link_token": LinkToken}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    account = get_account()
    LinkToken.deploy({"from": account})


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    # ↑ this account is the account if the parameter has been satisfied
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # ↑ brownie does the ABI compiling ↑
    # tx = link_token_contract.transfer(contract_address, amount {"from": account})
    tx.wait(1)
    print("Funding contract!")
    return tx


def deploy_arton_purchase():
    account = get_account()
    artonPurchase = ArtonPurchase.deploy(
        config["networks"][network.show_active()]["vrf_coordinator"],
        config["networks"][network.show_active()]["link_token"],
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    url = link[network.show_active()]
    print(f"The ArtonPurchase {network.show_active()} address: {url.format(artonPurchase)}")
    return artonPurchase


def raw_create_arton(eth_value, account):
    account = account if account else get_account()
    if len(ArtonPurchase) <= 0:
        artonPurchase = deploy_arton_purchase()
    else:
        artonPurchase = ArtonPurchase[-1]

    funding_tx = fund_with_link(
        contract_address=artonPurchase, amount=100000000000000000
    )
    funding_tx.wait(1)

    creating_tx = artonPurchase.rawCreateArton({"from": account, "value": eth_value})
    creating_tx.wait(1)

    print("The random number has been requested")

    return creating_tx


artonPurchase = ArtonPurchase[-1]


def create_2_digit_number(creating_tx):
    randomResult = str(artonPurchase.randomResult())
    print(f"Random result {randomResult}")

    level = creating_tx.events["LevelRequested"]["level"]
    print(f"The requested arton's level: {level}")
    to_be_set = 0
    outcome = []

    
    for i in range(0, (len(randomResult) - 1), 2):
        to_randomize = int(randomResult[i] + randomResult[i + 1])
        final_result = abs(random.randint(to_randomize - 10, to_randomize))
        outcome.append(str(final_result))

    print(f"outcome: {outcome}")
    print(f"randomResult is : {randomResult}")

    id = int(artonPurchase.id())
    id = id if (id < 76) else (id % 76)
    print(f"this is the id: {id}")

    if level == 1:
        j = 0
        for i in range(0, len(outcome) - id, 1):
            if (int(outcome[id + i]) > 10) and (int(outcome[id + i]) <= 30):
                #print(f"this runs 1")
                position = id + j
                to_be_set = int(outcome[position])
                print(f"to be set is: {to_be_set}")
                break
            j += 1
    elif level == 2:
        j = 0
        for i in range(0, len(outcome) - id, 1):
            if (int(outcome[id + i]) > 30) and (int(outcome[id + i]) <= 60):
                #print(f"this runs2")
                position = id + j
                to_be_set = int(outcome[position])
                print(f"to be set is: {to_be_set}")
                break
            j += 1
    else:
        to_be_set = int(outcome[id])
        #print("this runs 3")
        print(to_be_set)

    return to_be_set


def set_shortRandomNumber(account, eth_amount):
    owner_account = get_account()
    user_account = account if account != owner_account else owner_account
    artonPurchase = ArtonPurchase[-1]
    creating_tx = raw_create_arton(eth_value=eth_amount, account=user_account)
    creating_tx.wait(1)
    to_be_set = create_2_digit_number(creating_tx=creating_tx)
    print(f"Setting the shortRandomNumber to be:{to_be_set}")
    artonPurchase.setRandomNumber(to_be_set, {"from": owner_account})
    print(
        f"This is the shortRandomResult: {artonPurchase.shortRandomResult(), artonPurchase.randomResult()}"
    )
