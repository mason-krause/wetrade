import time


def lookup_error_msg(error_code, msg_ref='with', order_id=0):
  default_msg = f': Unknown error {msg_ref} order, check logs for more info'
  msg_dict = {
    1508: f': Price unavailable {msg_ref} (Order ID: {order_id}), waiting 1 sec then retrying',
    163: f': Processing error {msg_ref} (Order ID: {order_id}), waiting 1 sec then retrying',
    2084: f': Stop price out of range (Order ID: {order_id})- changing to market order and replacing',
    2085: f': Stop price out of range (Order ID: {order_id})- changing to market order and replacing',
    1524: f': Order {order_id} still updating, waiting 1 sec then retrying' }
  if error_code in msg_dict:
    return msg_dict[error_code]
  else:
    return default_msg
  
def lookup_user_msg(action, price=0.0, account_key='', order_response={}, old_id=0):
  if order_response == {}:
    return ''
  if action == 'place_order':
    return '{}: Placed {} order to {} {} shares of {} at ${} (Order ID: {}, Account: {})'.format(
      time.strftime('%H:%M:%S', time.localtime()),
      order_response['Order'][0]['priceType'],
      order_response['Order'][0]['Instrument'][0]['orderAction'],
      order_response['Order'][0]['Instrument'][0]['quantity'],
      order_response['Order'][0]['Instrument'][0]['Product']['symbol'],
      price,
      order_response['OrderIds'][0]['orderId'],
      account_key)
  elif action == 'update_price':
    return '{}: Placed updated {} order to {} {} shares of {} at ${} (Order ID: {}, Account: {})'.format(
      time.strftime('%H:%M:%S', time.localtime()),
      order_response['Order'][0]['priceType'],
      order_response['Order'][0]['Instrument'][0]['orderAction'],
      order_response['Order'][0]['Instrument'][0]['quantity'],
      order_response['Order'][0]['Instrument'][0]['Product']['symbol'],
      price,
      order_response['OrderIds'][0]['orderId'],
      account_key)
  elif action == 'to_market_order':
    return '{}: Changed Order {} to market order (Order ID: {}, Account: {})'.format(
      time.strftime('%H:%M:%S', time.localtime()),
      old_id,
      order_response['OrderIds'][0]['orderId'],
      account_key)