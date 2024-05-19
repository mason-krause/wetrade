import time
import datetime
from wetrade.api import APIClient
from wetrade.utils import log_in_background, check_market_hours, start_thread

class MultiQuote:
  def __init__(self, client:APIClient, symbols:tuple):
    self.client = client
    self.symbols = symbols
    self.symbol_str = ', '.join(self.symbols)
    self.last_prices = {}
    self.monitoring_active = False

  def get_quote(self):
    response, status_code = self.client.request_quote(symbol=self.symbol_str)
    try:
      quote_data = response['QuoteResponse']['QuoteData']
      return quote_data
    except Exception as e:
      log_in_background(
        called_from = 'get_quote',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + ': Error getting quote, retrying',
        e = e,
        symbol = self.symbol)
      time.sleep(.5)
      return self.get_quote()
   
  def get_last_price(self):
    quote_data = self.get_quote()
    for quote in quote_data:
      symbol = quote['Product']['symbol']
      self.last_prices[symbol] =  quote['All']['lastTrade'] 
    return self.last_prices

  def monitor_quote(self):
    if self.monitoring_active == False:
      market_close = check_market_hours()['close']
      if time.strftime('%H:%M', time.localtime()) > market_close:
        log_in_background(
          called_from = 'monitor_quote',
          tags = ['user-message'], 
          symbol = self.symbol,
          message = '{}: Markets are closed'.format(time.strftime('%H:%M:%S', time.localtime())))
      else:
        self.monitoring_active = True
      while self.monitoring_active == True and time.strftime('%H:%M', time.localtime()) < market_close:
        self.get_last_price()
        time.sleep(.5)
      self.monitoring_active = False
      
  def monitor_in_background(self):
    start_thread(self.monitor_quote)
  
  def wait_for_price_fall(self, symbol, target_price, func=None, func_args=[], func_kwargs={}):
    self.monitor_in_background()
    while self.last_prices[symbol] > target_price and self.monitoring_active == True:
      time.sleep(1)
    func(*func_args, **func_kwargs)

  def run_below_price(self, symbol, target_price, func, func_args=[], func_kwargs={}):
    args = [symbol, target_price, func, func_args, func_kwargs]
    start_thread(self.wait_for_price_fall, args=args)

  def wait_for_price_rise(self, symbol, target_price, func=None, func_args=[], func_kwargs={}):
    self.monitor_in_background()
    while self.last_prices[symbol] < target_price and self.monitoring_active == True:
      time.sleep(1)
    func(*func_args, **func_kwargs)

  def run_above_price(self, symbol, target_price, func, func_args=[], func_kwargs={}):
    args = [symbol, target_price, func, func_args, func_kwargs]
    start_thread(self.wait_for_price_rise, args=args)