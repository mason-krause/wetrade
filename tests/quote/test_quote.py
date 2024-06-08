import time
from wetrade.quote import Quote
from tests.mock_api import MockAPIClient as APIClient


class TestQuote:
  @classmethod
  def setup_class(cls):
    client = APIClient()
    cls.quote = Quote(client=client, symbol='GOOG')

  def test_get_quote(self):
    quote = self.quote.get_quote()
    quote_symbol = quote['Product']['symbol']
    assert quote_symbol == self.quote.symbol, 'Error getting quote data'
    
  def test_get_open(self):
    open = self.quote.get_open()
    assert open == 578.89, 'Error getting open price'
    
  def test_get_last_price(self):
    last_price = self.quote.get_last_price()
    assert last_price in (577.51, 700.50, 800.75), 'Error getting last price'
    assert self.quote.last_price == last_price, 'Error setting last price'

  def test_monitor_in_background(self):
    self.quote.monitor_in_background()
    if self.quote.market_hours.market_has_closed() == False:
      time.sleep(3)
      assert self.quote.last_price == 800.75, 'Error monitoring quote'
      self.quote.monitoring_active = False

