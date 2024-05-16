import google.cloud.logging
from wetrade.api import APIClient
from wetrade.account import Account
from wetrade.quote import Quote
from settings import enable_cloud_logging


def main():
  if enable_cloud_logging == True:
    client = google.cloud.logging.Client()
    client.setup_logging()
  
  client = APIClient()

  account = Account(client=client)
  print('My Account Key: ', account.account_key)
  print('My Balance: ', account.check_balance())

  quote = Quote(client=client, symbol='AAPL')
  print('Last Quote Price: ', quote.get_last_price())


if __name__ == '__main__':
  main()