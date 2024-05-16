import unittest
from wetrade.account import Account
from tests.mock_api import MockAPIClient as APIClient


class TestAccount(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    client = APIClient()
    cls.account = Account(client=client, account_key='vQMsebA1H5WltUfDkJP48g')

  def test_list_accounts(self):
    account_list = self.account.list_accounts()
    first_account_id = account_list[0]['accountId']
    self.assertEqual(
      first_account_id,
      '823145980',
      'Error getting account list')

  def test_check_balance(self):
    balance = self.account.check_balance()
    self.assertEqual(
      balance,
      5000.0,
      'Error getting account balance')

  def test_view_portfolio(self):
    portfolio = self.account.view_portfolio()
    third_position_symbol = portfolio[0]['Position'][2]['Product']['symbol']
    self.assertEqual(
      third_position_symbol,
      'MSFT',
      'Error getting account portfolio')
