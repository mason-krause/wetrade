import random
import time
from wetrade.order import StopOrder
from wetrade.utils import log_in_background
from .lookup_msg import lookup_error_msg


# Stop order that converts to a market order if rejected or out of range 
class ConvertingStopOrder(StopOrder):
  '''
  A stop order that converts to a limit order when rejected or current price is above stop price for a sell order or when current price is below stop price for a buy order
  '''
  def __handle_rejected_order(self):
    self.updating = True
    self.client_order_id = random.randint(1000000000, 9999999999)
    self.order_type =  'MARKET'
    self.preview_order_request['PreviewOrderRequest']['Order']['priceType'] = 'MARKET'
    self.place_order()
    self.updating = False
    log_in_background(
      called_from = 'wait_for_status',
      tags = ['user-message'], 
      account_key = self.account_key,
      symbol = self.symbol,
      message = '{}: Order {} REJECTED , replacing as MARKET order (Account: {})'.format(time.strftime('%H:%M:%S', time.localtime()), self.order_id, self.account_key))
    
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
      elif error_code in (2084, 2085):
        self.order_type =  'MARKET'
        self.preview_order_request['PreviewOrderRequest']['Order']['priceType'] = 'MARKET'
        return self.__modify_order(action_type)
