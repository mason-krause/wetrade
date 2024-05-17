from wetrade.api import APIClient
from wetrade.account import Account
from wetrade.quote import Quote
from wetrade.order import LimitOrder
from wetrade.utils import setup_logging


def main():
  setup_logging()
  client = APIClient()

  account = Account(client=client)
  print('My Account Key: ', account.account_key)
  print('My Balance: ', account.check_balance())

  quote = Quote(client=client, symbol='AAPL')
  print('Last Quote Price: ', quote.get_last_price())


if __name__ == '__main__':
  main()