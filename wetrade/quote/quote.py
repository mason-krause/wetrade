import time
import datetime
from wetrade.api import APIClient
from wetrade.market_hours import MarketHours
from wetrade.utils import log_in_background, start_thread

class Quote:
  '''
  A simple Quote for tracking one security

  :param APIClient client: your :ref:`APIClient <api_client>`
  :param str symbol: the symbol of your security
  '''
  def __init__(self, client:APIClient, symbol):
    self.client = client
    self.symbol = symbol
    self.last_price = 0.0
    self.monitoring_active = False
    self.market_hours = MarketHours()

  def get_quote(self):
    '''
    Gets the most recent quote details for your security
    '''
    response, status_code = self.client.request_quote(symbol=self.symbol)
    try:
      quote_data = response['QuoteResponse']['QuoteData'][0]
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
    
  def get_open(self):
    '''
    Returns the opening price for your security during the current session
    '''
    return self.get_quote()['All']['open']   
   
  def get_last_price(self):
    '''
    Gets the most recent price for your security
    '''
    self.last_price =  self.get_quote()['All']['lastTrade'] 
    return self.last_price

  def __monitor_quote(self):
    if self.monitoring_active == False:
      if self.market_hours.market_has_closed() == False:
        self.monitoring_active = True
      while self.monitoring_active == True and self.market_hours.market_has_closed() == False:
        quote_data = self.get_quote()
        self.last_price = quote_data['All']['lastTrade']
        time.sleep(.5)
      self.monitoring_active = False
      
  def monitor_in_background(self):
    '''
    Monitors quote details in a new thread to keep Quote.last_price up to date 
    '''
    start_thread(self.__monitor_quote)
  
  def wait_for_price_fall(self, target_price, then=None, args=[], kwargs={}):
    '''
    Waits for your security to fall below a certain price then optionally runs a callback function 

    :param float target_price: your set target price
    :param then: (optional) a callback function to run when price falls below target
    :param list args: a list of args for your func
    :param dict kwargs: a dict containing kwargs for your func
    '''
    self.monitor_in_background()
    waiting = True
    while waiting and self.monitoring_active == True:
      if self.last_price < target_price:
        waiting = False
        if then:
          then(*args, **kwargs)
      time.sleep(.2)

  def run_below_price(self, target_price, func, func_args=[], func_kwargs={}):
    '''
    Runs a callback when your security falls below a certain price without waiting

    :param float target_price: your set target price
    :param func: a function to run when price falls below target
    :param list func_args: a list of args for your func
    :param dict func_kwargs: a dict containing kwargs for your func
    '''
    args = [target_price, func, func_args, func_kwargs]
    start_thread(self.wait_for_price_fall, args=args)

  def wait_for_price_rise(self, target_price, then=None, args=[], kwargs={}):
    '''
    Waits for your security to rise above a certain price then optionally runs a callback function 

    :param float target_price: your set target price
    :param then: (optional) a callback function to run when price rises above target
    :param list args: a list of args for your func
    :param dict kwargs: a dict containing kwargs for your func
    '''
    self.monitor_in_background()
    waiting = True
    while waiting and self.monitoring_active == True:
      if self.last_price > target_price:
        waiting = False
        if then:
          then(*args, **kwargs)
      time.sleep(.2)

  def run_above_price(self, target_price, func, func_args=[], func_kwargs={}):
    '''
    Runs a callback when your security rises above a certain price without waiting

    :param float target_price: your set target price
    :param func: a function to run when price rises above target
    :param list func_args: a list of args for your func
    :param dict func_kwargs: a dict containing kwargs for your func
    '''
    args = [target_price, func, func_args, func_kwargs]
    start_thread(self.wait_for_price_rise, args=args)