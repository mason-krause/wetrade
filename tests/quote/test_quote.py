import pytest
import time
from wetrade.quote import Quote
from tests.mock_api import MockAPIClient as APIClient
from unittest.mock import patch, MagicMock


@patch('wetrade.market_hours.MarketHours.market_has_closed', MagicMock(return_value=False))
class TestQuote:
  @classmethod
  def setup_class(cls):
    client = APIClient()
    cls.quote = Quote(client=client, symbol='GOOG')

  @classmethod
  def teardown_class(cls):
    cls.quote.monitoring_active = False

  def setup_method(self):
    self.quote.client.reset_quote_queue()
    self.quote.monitoring_active = False

  def test_get_quote(self):
    quote = self.quote.get_quote()
    quote_symbol = quote['Product']['symbol']
    assert quote_symbol == self.quote.symbol, 'Error getting quote data'
    
  def test_get_open(self):
    open = self.quote.get_open()
    assert open == 578.89, 'Error getting open price'
    
  def test_get_last_price(self):
    last_price = self.quote.get_last_price()
    assert last_price in (577.51, 200.1, 700.50, 800.75), 'Error getting last price'
    assert self.quote.last_price == last_price, 'Error setting last price'

  def test_monitor_in_background(self):
    self.quote.monitor_in_background()
    time.sleep(4)
    assert self.quote.last_price == 800.75, 'Error monitoring quote'
  
  @pytest.mark.timeout(10)
  def test_wait_for_price_fall(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.wait_for_price_fall(250.75, then=func)
    assert waiting == False, 'Error waiting for status'

  def test_run_below_price(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.run_below_price(250.75, func=func)
    time.sleep(2)
    assert waiting == False, 'Error waiting for status'  

  @pytest.mark.timeout(10)
  def test_wait_for_price_rise(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.wait_for_price_rise(650.75, then=func)
    assert waiting == False, 'Error waiting for status'

  def test_run_above_price(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.run_above_price(650.75, func=func)
    time.sleep(2)
    assert waiting == False, 'Error waiting for status'


