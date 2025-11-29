import time

  
def lookup_user_msg(action, price=0.0, account_key='', order_response={}, old_id=0):
  if order_response == {}:
    return ''
  if action == 'place_order':
    return '{}: Placed {} order to {} {} for {} contracts of {} with a ${} {} amount (Order ID: {}, Account: {})'.format(
      time.strftime('%H:%M:%S', time.localtime()),
      order_response['Order'][0]['priceType'],
      order_response['Order'][0]['Instrument'][0]['orderAction'].split('_')[1],
      order_response['orderType'],
      order_response['Order'][0]['Instrument'][0]['quantity'],
      order_response['Order'][0]['Instrument'][0]['Product']['symbol'],
      price,
      order_response['Order'][0]['priceType'],
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