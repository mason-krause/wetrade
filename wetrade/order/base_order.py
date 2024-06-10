import time
import random
from contextlib import suppress
from wetrade.api import APIClient
from wetrade.utils import start_thread, log_in_background
from .lookup_msg import lookup_error_msg, lookup_user_msg


class BaseOrder:
  '''
  A base order class containing methods use in other order types

  :param APIClient client: your :ref:`APIClient <api_client>`
  :param str account_key: your account key
  :param str symbol: the symbol of your security
  :param str action: The action for your order (BUY, SELL, BUY_TO_COVER, SELL_SHORT, BUY_OPEN, BUY_CLOSE, SELL_OPEN, SELL_CLOSE, EXCHANGE)
  :param int quantity: the quantity for your order
  :param float price: the price for your order
  '''
  def __init__(self, client:APIClient, account_key, symbol, action, quantity, price):
    self.client = client
    self.account_key = account_key
    self.symbol = symbol
    self.action = action
    self.quantity = quantity
    self.price = price
    self.order_type = self.order_type if hasattr(self, 'order_type') else 'LIMIT'
    self.security_type = self.security_type if hasattr(self, 'security_type') else 'EQ'
    self.client_order_id = random.randint(1000000000, 9999999999)
    self.order_id = 0
    self.updating = False
    self.status = ''
    self.preview_order_request = {
      'PreviewOrderRequest': {
        'orderType': self.security_type, # [EQ, OPTN, SPREADS, BUY_WRITES, BUTTERFLY, IRON_BUTTERFLY, CONDOR, IRON_CONDOR, MF, MMF]
        'clientOrderId': self.client_order_id,
        'Order': {
          'allOrNone': 'false',
          'priceType': self.order_type, # [MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP_CNST_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_TRAILING_STOP_CNST, TRAILING_STOP_PRCT_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_TRAILING_STOP_PRCT, TRAILING_STOP_CNST, TRAILING_STOP_PRCT, HIDDEN_STOP, HIDDEN_STOP_BY_LOWER_TRIGGER, UPPER_TRIGGER_BY_HIDDEN_STOP, NET_DEBIT, NET_CREDIT, NET_EVEN, MARKET_ON_OPEN, MARKET_ON_CLOSE, LIMIT_ON_OPEN, LIMIT_ON_CLOSE]
          'orderTerm': 'GOOD_FOR_DAY', # [GOOD_UNTIL_CANCEL, GOOD_FOR_DAY, GOOD_TILL_DATE, IMMEDIATE_OR_CANCEL, FILL_OR_KILL]
          'marketSession': 'REGULAR',
          'stopPrice': self.price,
          'limitPrice': self.price,
          'stopLimitPrice': self.price,
          'Instrument': {
            'Product': {
              'securityType': 'EQ',
              'symbol': self.symbol},
            'orderAction': self.action, # [BUY, SELL, BUY_TO_COVER, SELL_SHORT, BUY_OPEN, BUY_CLOSE, SELL_OPEN, SELL_CLOSE, EXCHANGE]
            'quantityType': 'QUANTITY',
            'quantity': self.quantity}}}}
    self.place_order_request = {}
    self.disable_await_status = False

  def __modify_order(self, action_type='preview'):
    if action_type == 'preview':
      response, status_code = self.client.request_order_preview(account_key=self.account_key, order_data=self.preview_order_request)
      response_key = 'PreviewOrderResponse'
      msg_ref = 'previewing'
    elif action_type == 'place':
      response, status_code = self.client.request_order_place(account_key=self.account_key, order_data=self.place_order_request)
      response_key = 'PlaceOrderResponse'
      msg_ref = 'placing'
    elif action_type == 'preview_update':
      response, status_code = self.client.request_order_change_preview(account_key=self.account_key, order_id=self.order_id, order_data=self.preview_order_request)
      response_key = 'PreviewOrderResponse'
      msg_ref = 'previewing updated'
    elif action_type == 'update':
      response, status_code = self.client.request_order_change_place(account_key=self.account_key, order_id=self.order_id, order_data=self.place_order_request)
      response_key = 'PlaceOrderResponse'
      msg_ref = 'updating'
    else:
      return # maybe log incorrect action specified  
    if response_key in response:
      return response[response_key]
    elif 'Error' in response:
      error_code = response['Error']['code']
      error_msg = lookup_error_msg(error_code=error_code, msg_ref=msg_ref, order_id=self.order_id)
      log_in_background(
        called_from = '__modify_order',
        tags = ['user-message'], 
        message = time.strftime('%H:%M:%S', time.localtime()) + error_msg,
        account_key = self.account_key,
        symbol = self.symbol)
      if error_code in (1508, 163, 1524):
        time.sleep(1)
        return self.__modify_order(action_type)

  def preview_order(self):
    preview_response = self.__modify_order('preview')
    if preview_response:
      self.place_order_request = {
        'PlaceOrderRequest': {
          'orderType': preview_response['orderType'],
          'clientOrderId': self.client_order_id,
          'PreviewIds': preview_response['PreviewIds'],
          'Order': preview_response['Order']}}
    return preview_response
  
  def place_order(self):
    '''Places your order'''
    preview = self.preview_order()
    if preview:
      order_response = self.__modify_order('place')
      if order_response:
        self.order_id = order_response['OrderIds'][0]['orderId']
        log_in_background(
          called_from = 'place_order',
          tags = ['user-message'], 
          account_key = self.account_key,
          symbol = self.symbol,
          message = lookup_user_msg('place_order', price=self.price, account_key= self.account_key, order_response=order_response))
      return order_response
  
  def preview_update_price(self, new_price):
    self.client_order_id = random.randint(1000000000, 9999999999)
    self.preview_order_request['PreviewOrderRequest']['Order']['priceType'] = self.order_type
    self.preview_order_request['PreviewOrderRequest']['Order']['limitPrice'] = new_price
    self.preview_order_request['PreviewOrderRequest']['Order']['stopPrice'] = new_price
    self.preview_order_request['PreviewOrderRequest']['Order']['stopLimitPrice'] = new_price
    preview_response = self.__modify_order('preview_update')
    if preview_response:
      self.place_order_request = {
        'PlaceOrderRequest': {
          'orderType': preview_response['orderType'],
          'clientOrderId': self.client_order_id,
          'PreviewIds': preview_response['PreviewIds'],
          'Order': preview_response['Order']}}
    return preview_response
  
  def update_price(self, new_price):
    '''
    Updates the price of an already placed order
    
    :param float new_price: the new price for your order
    '''
    old_id = self.order_id
    self.updating = True
    preview = self.preview_update_price(new_price)
    if preview:
      order_response = self.__modify_order('update')
      if order_response:
        self.order_id = order_response['OrderIds'][0]['orderId']
        self.price = new_price
        log_in_background(
          called_from = 'update_price',
          tags = ['user-message'], 
          account_key = self.account_key,
          symbol = self.symbol,
          message = lookup_user_msg('update_price', price=self.price, account_key=self.account_key, order_response=order_response, old_id=old_id))
      self.updating = False
      return order_response
    self.updating = False
  
  def to_market_order(self):
    '''Converts an active, already-placed order into a market order which will execute immediately during market hours'''
    old_id = self.order_id
    self.updating = True
    self.order_type = 'MARKET'
    preview = self.preview_update_price(0.0)
    if preview:
      order_response = self.__modify_order('update')
      if order_response:
        self.order_id = order_response['OrderIds'][0]['orderId']
        log_in_background(
          called_from = 'to_market_order',
          tags = ['user-message'], 
          account_key = self.account_key,
          symbol = self.symbol,
          message = lookup_user_msg('to_market_order', price=self.price, account_key=self.account_key, order_response=order_response, old_id=old_id))
      self.updating = False
      return order_response
    self.updating = False

  def cancel_order(self):
    '''Cancels your active, already-placed order'''
    response, status_code = self.client.request_order_cancel(account_key=self.account_key, order_id=self.order_id, symbol=self.symbol)
    msg_num = 0
    with suppress(Exception):
      msg_num = response['CancelOrderResponse']['Messages']['Message'][0]['code']
    if msg_num in (5011, 4186):
      log_in_background(
        called_from = 'cancel_order',
        tags = ['user-message'], 
        account_key = self.account_key,
        symbol = self.symbol,
        message = '{}: Requested to cancel order {} (Account: {})'.format(
          time.strftime('%H:%M:%S', time.localtime()),
          response['CancelOrderResponse']['orderId'],
          self.account_key))
      return True
    else:
      log_in_background(
        called_from = 'cancel_order',
        tags = ['user-message'], 
        account_key = self.account_key,
        symbol = self.symbol,
        message = '{}: Could not cancel order {} (Account: {}), check logs'.format(
          time.strftime('%H:%M:%S', time.localtime()),
          response['CancelOrderResponse']['orderId'],
          self.account_key))
      return False

  def check_status(self):
    '''Checks the status of an already placed order'''
    response, status_code = self.client.request_order_status(account_key=self.account_key, order_id=self.order_id, symbol=self.symbol)
    status = ''
    execution_price = 0.0
    with suppress(Exception):
      status = response['OrdersResponse']['Order'][0]['OrderDetail'][0]['status']
      execution_price = response['OrdersResponse']['Order'][0]['OrderDetail'][0]['Instrument'][0]['averageExecutionPrice']
    if status == 'EXECUTED' and execution_price != 0:
      self.price = execution_price
    self.status = status
    return status

  def __handle_rejected_order(self):
    # # Need to reset client_order_id after rejection to resend, etc (see example below)
    # self.updating = True
    # self.client_order_id = random.randint(1000000000, 9999999999)
    # # Make any changes here
    # self.place_order()
    # self.updating = False
    log_in_background(
      called_from = 'wait_for_status',
      tags = ['user-message'], 
      account_key = self.account_key,
      symbol = self.symbol,
      message = '{}: Order {} REJECTED - no longer waiting (Account: {})'.format(time.strftime('%H:%M:%S', time.localtime()), self.order_id, self.account_key))

  def wait_for_status(self, status, then=None, args=[], kwargs={}): # [OPEN, EXECUTED, CANCELLED, INDIVIDUAL_FILLS, CANCEL_REQUESTED, EXPIRED, REJECTED]
    '''
    Waits for your order to reach your specified status then runs an optional callback function
    
    :param str status: the status to wait for (OPEN, EXECUTED, CANCELLED, INDIVIDUAL_FILLS, CANCEL_REQUESTED, EXPIRED, REJECTED)
    :param then: (optional) a callback function to run after waiting for status
    :param list args: a list of args for your function
    :param dict kwargs: a dict containing kwargs for your function
    '''
    waiting = True
    stop_for = ('CANCELLED','EXECUTED','EXPIRED')
    while waiting and self.disable_await_status == False:
      if self.updating == False:
        order_status = self.check_status()
        if order_status == 'REJECTED': # special handling for rejected orders
          return self.__handle_rejected_order()
        if order_status == 'CANCELLED': # Double check canceled order for corner case waiting on new order_id
          time.sleep(1)
          order_status = self.check_status()
        if order_status == status:
          waiting = False
          if then:
            return then(*args, **kwargs)
          else:
            return
        elif order_status in stop_for:
          waiting = False
          log_in_background(
            called_from = 'wait_for_status',
            tags = ['user-message'], 
            account_key = self.account_key,
            symbol = self.symbol,
            message = '{}: Order {} {} - no longer waiting (Account: {})'.format(time.strftime('%H:%M:%S', time.localtime()), self.order_id, order_status, self.account_key))
          return
      time.sleep(.4) # throttle to avoid rate limit 

  def run_when_status(self, status, func, func_args=[], func_kwargs={}):
    '''
    Runs a callback when your order reaches a certain status without waiting
    
    :param str status: your anticipated status (OPEN, EXECUTED, CANCELLED, INDIVIDUAL_FILLS, CANCEL_REQUESTED, EXPIRED, REJECTED)
    :param then: (optional) a callback function to run after status is met
    :param list args: a list of args for your function
    :param dict kwargs: a dict containing kwargs for your function
    '''
    args = [status, func, func_args, func_kwargs]
    start_thread(self.wait_for_status, args=args)