import datetime
from copy import deepcopy
from wetrade.utils import log_in_background
from wetrade.api import APIClient
from .. import BaseOrder
from .lookup_options_msg import lookup_user_msg

class CreditSpreadOrder(BaseOrder):
  '''An order for a put or call spread order'''
  def __init__(self, client:APIClient, account_key, action:str, option_type, symbol, expiry_date, quantity, net_credit_amount, buy_strike_price, sell_strike_price):
    self.order_type = 'NET_CREDIT'
    expiry_str = expiry_date
    if option_type not in ['Call', 'Put']:
      raise ValueError('action must be "Call" or "Put"')
    if action.upper() not in ['OPEN', 'CLOSE']:
      raise ValueError('action must be "OPEN" or "CLOSE"')
    if isinstance(expiry_date, datetime.datetime) or isinstance(expiry_date, datetime.date):
      expiry_str = expiry_date.strftime("%m-%d-%Y")
    if not isinstance(expiry_str, str):
      raise TypeError('expiry_date must be a string, datetime, or date')
    else:
      split_expiry_str= expiry_str.split('-')
      if len(split_expiry_str) != 3:
        raise ValueError('expiry_date strings must be formatted MM-DD-YYYY')
      self.expiry_month = split_expiry_str[0]
      self.expiry_day = split_expiry_str[1]
      self.expiry_year = split_expiry_str[2]
    BaseOrder.__init__(self, client, account_key, symbol, quantity=quantity, price=net_credit_amount, action='BUY_' + action.upper(), security_type='SPREADS')
    self.lookup_user_msg = lookup_user_msg
    self.action = action
    self.preview_order_request['PreviewOrderRequest']['Order']['allOrNone'] = 'true'
    self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'][0]['Product']['callPut'] = option_type
    self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'][0]['Product']['expiryYear'] = self.expiry_year
    self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'][0]['Product']['expiryMonth'] = self.expiry_month
    self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'][0]['Product']['expiryDay'] = self.expiry_day
    self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'][0]['Product']['strikePrice'] = buy_strike_price
    new_instrument = deepcopy(self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'][0])
    new_instrument['orderAction'] = 'SELL_' + action.upper()
    new_instrument['Product']['strikePrice'] = sell_strike_price
    self.preview_order_request['PreviewOrderRequest']['Order']['Instrument'].append(new_instrument)
  
  def to_market_order(self):
    log_in_background(
      called_from = 'to_market_order',
      tags = ['user-message'], 
      account_key = self.account_key,
      symbol = self.symbol,
      message = '{}: to_market_order is not availible for Options Spreads'.format(
        datetime.datetime.now().strftime('%H:%M:%S')))
    
  def update_price(self, new_price):
    log_in_background(
      called_from = 'update_price',
      tags = ['user-message'], 
      account_key = self.account_key,
      symbol = self.symbol,
      message = '{}: update_price is not availible for Options Spreads'.format(
        datetime.datetime.now().strftime('%H:%M:%S')))