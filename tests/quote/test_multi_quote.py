import pytest
import time
from wetrade.quote import MultiQuote
from tests.mock_api import MockAPIClient as APIClient
from unittest.mock import patch, MagicMock


@patch('wetrade.market_hours.MarketHours.market_has_closed', MagicMock(return_value=False))
class TestMultiQuote:
  @classmethod
  def setup_class(cls):
    client = APIClient()
    cls.quote = MultiQuote(client=client, symbols=('TSLA', 'NVDA'))

  @classmethod
  def teardown_class(cls):
    cls.quote.monitoring_active = False

  def setup_method(self):
    self.quote.client.reset_multiquote_queue()
    self.quote.monitoring_active = False

  def test_get_quote(self):
    quote = self.quote.get_quote()
    symbol_a = quote[0]['Product']['symbol']
    symbol_b = quote[1]['Product']['symbol']
    assert symbol_a == self.quote.symbols[0], 'Error getting quote data'
    assert symbol_b == self.quote.symbols[1], 'Error getting quote data'
    
  def test_get_last_price(self):
    last_price = self.quote.get_last_price()
    assert 'TSLA' in last_price, 'Error getting last price'
    assert 'NVDA' in last_price, 'Error getting last price'
    assert last_price['TSLA'] in (175.50, 210.50), 'Error getting last price'
    assert last_price['NVDA'] in (750.45, 1050.45), 'Error getting last price'

  def test_monitor_in_background(self):
    self.quote.monitor_in_background()
    time.sleep(4)
    assert self.quote.last_prices['TSLA'] == 210.50, 'Error monitoring quote'
    assert self.quote.last_prices['NVDA'] == 1050.45, 'Error monitoring quote'
  
  @pytest.mark.timeout(10)
  def test_wait_for_price_fall(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.wait_for_price_fall(
      symbol= 'TSLA',
      target_price=100.75, 
      then=func)
    assert waiting == False, 'Error waiting for status'

  def test_run_below_price(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.run_below_price(
      symbol= 'TSLA',
      target_price=100.75, 
      func=func)
    time.sleep(2)
    assert waiting == False, 'Error waiting for status'  

  @pytest.mark.timeout(10)
  def test_wait_for_price_rise(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.wait_for_price_rise(
      symbol= 'NVDA',
      target_price=900.75, 
      then=func)
    assert waiting == False, 'Error waiting for status'

  def test_run_above_price(self):
    waiting = True
    def func():
      nonlocal waiting
      waiting = False
    self.quote.run_above_price(
      symbol= 'NVDA',
      target_price=900.75, 
      func=func)
    time.sleep(3)
    assert waiting == False, 'Error waiting for status'  