from brownie import ArtonPurchase


def main():
    artonPurchase = ArtonPurchase[-1]
    random_result = artonPurchase.shortRandomResult()
    randy = artonPurchase.randomResult()
    print(f"The random number is: {random_result, randy}")
