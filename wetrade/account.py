import time
from wetrade.api import APIClient
from wetrade.utils import log_in_background

class Account:
  def __init__(self, client:APIClient, account_key=''):
    self.client = client
    self.account_key = account_key if account_key else self.list_accounts()[0]['accountIdKey']

  def list_accounts(self):
    response, status_code = self.client.request_account_list()
    try:
      accounts = response['AccountListResponse']['Accounts']['Account']
      return accounts
    except Exception as e:
      log_in_background(
        called_from = 'list_accounts',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting account list, retrying',
        e = e,
        account_key = self.account_key)
      return self.list_accounts()

  def check_balance(self):
    response, status_code = self.client.request_account_balance(account_key=self.account_key)
    try:
      balance = response['BalanceResponse']['Computed']['cashAvailableForInvestment']
      return balance
    except Exception as e:
      log_in_background(
        called_from = 'list_accounts',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting account balance, retrying',
        e = e,
        account_key = self.account_key)
      return self.check_balance()

  def view_portfolio(self):
    response, status_code = self.client.request_account_portfolio(account_key=self.account_key)
    try:
      portfolio = {} if status_code == 204 else response['PortfolioResponse']['AccountPortfolio']
      return portfolio
    except Exception as e:
      log_in_background(
        called_from = 'list_accounts',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting portfolio, retrying',
        e = e,
        account_key = self.account_key)
      return self.view_portfolio()