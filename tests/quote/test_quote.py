import unittest
from wetrade.quote import Quote
from tests.mock_api import MockAPIClient as APIClient


class TestQuote(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    client = APIClient()
    cls.quote = Quote(client=client, symbol='GOOG')

  def test_get_quote(self):
    quote = self.quote.get_quote()
    quote_symbol = quote['Product']['symbol']
    self.assertEqual(
      quote_symbol,
      self.quote.symbol,
      'Error getting quote data')
    
  def test_get_open(self):
    open = self.quote.get_open()
    self.assertEqual(
      open,
      578.89,
      'Error getting open price')
    
  def test_get_last_price(self):
    last_price = self.quote.get_last_price()
    with self.subTest():
      self.assertEqual(
        last_price,
        577.51,
        'Error getting last price')
    with self.subTest():
      self.assertEqual(
        self.quote.last_price,
        577.51,
        'Error setting last price')


