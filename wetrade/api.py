import xmltodict
from wetrade.utils import parse_response_data, log_in_background
from wetrade.user_session import UserSession


class APIClient:
  '''
  :param UserSession session: (optional) supply your own UserSession for a custom configuration. By default, a new UserSession will be created automatically
  '''
  def __init__(self, session=None):
    self.session = UserSession() if session==None else session

  def request_account_list(self):
    '''
    Provides details on all brokerage accounts connected to the active E-Trade user account
    '''
    url = self.session.config['base_url'] + 'v1/accounts/list.json'
    r = self.session.get(url=url)
    log_in_background(
      called_from = 'request_account_list', 
      url = url,
      r = r)
    return (parse_response_data(r), r.status_code)

  def request_account_balance(self, account_key):
    '''
    Provides details on the balance for a specified account

    :param str account_key: your specified account key
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/balance.json'.format(account_key)
    params = {'instType': 'BROKERAGE', 'realTimeNAV': 'true'}
    r = self.session.get(url=url, params=params)
    log_in_background(
      called_from = 'request_account_balance', 
      url = url,
      r = r,
      account_key = account_key)
    return (parse_response_data(r), r.status_code)

  def request_account_portfolio(self, account_key):
    '''
    Provides details on the portfolio for a specified account

    :param str account_key: your specified account key
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/portfolio.json'.format(account_key)
    r = self.session.get(url=url)
    log_in_background(
      called_from = 'request_account_portfolio', 
      url = url,
      r = r,
      account_key = account_key)
    return (parse_response_data(r), r.status_code)
  
  def request_account_orders(self, account_key, start_date='', end_date='', marker=''):
    '''
    Provides details on all of the orders placed by a specified account in a 
    given time frame.

    :param str account_key: your specified account key
    :param str start_date: the beginning date of your query; format: '%m%d%Y'
    :param str end_date: the last date of your query; format: '%m%d%Y'
    :param str marker: used to access multi-page results
    '''
    params = {}
    if start_date != '':
      params['fromDate'] = start_date
    if end_date != '':
      params['toDate'] = end_date
    if marker != '':
      params['marker'] = marker
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders.json'.format(account_key)
    r = self.session.get(url=url, params=params)
    log_in_background(
      called_from = 'request_account_orders', 
      url = url,
      r = r,
      account_key = account_key)
    return (parse_response_data(r), r.status_code)

  def request_quote(self, symbol):
    '''
    Provides live quote details for a specified symbol

    :param str symbol: the symbol of your security or a URL-encoded, comma-separated string for a list of securities 
    '''
    url = self.session.config['base_url'] + 'v1/market/quote/{}.json'.format(symbol)
    params = {'detailFlag': 'ALL'} # [ALL, WEEK_52, FUNDAMENTAL, INTRADAY, OPTIONS, MF_DETAIL]
    r = self.session.get(url=url, params=params)
    log_in_background(
      called_from = 'request_quote', 
      url = url,
      r = r,
      symbol = symbol)
    return (parse_response_data(r), r.status_code)
  
  def request_order_preview(self, account_key, order_data):
    '''
    Requests an E-Trade order preview. This is required before placing an order

    :param str account_key: your specified account key
    :param dict order_data: a dict containing an E-Trade `PreviewOrderRequest <https://apisb.etrade.com/docs/api/order/api-order-v1.html#/definitions/PreviewOrderRequest/>`__
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/preview.json'.format(account_key)
    headers = {'Content-Type': 'application/xml'}
    payload = xmltodict.unparse(order_data)
    r = self.session.post(url=url, headers=headers, data=payload)
    log_in_background(
      called_from = 'request_order_preview', 
      url = url,
      r = r,
      account_key = account_key,
      symbol = order_data['PreviewOrderRequest']['Order']['Instrument']['Product']['symbol'])
    return (parse_response_data(r), r.status_code)  
  
  def request_order_place(self, account_key, order_data):
    '''
    Places an order after an order preview

    :param str account_key: your specified account key
    :param dict order_data: a dict containing an E-Trade `PlaceOrderRequest <https://apisb.etrade.com/docs/api/order/api-order-v1.html#/definitions/PlaceOrderRequest/>`__
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/place.json'.format(account_key)
    headers = {'Content-Type': 'application/xml'}
    payload = xmltodict.unparse(order_data)
    r = self.session.post(url=url, headers=headers, data=payload)
    log_in_background(
      called_from = 'request_order_place', 
      url = url,
      r = r,
      account_key = account_key,
      symbol = order_data['PlaceOrderRequest']['Order'][0]['Instrument'][0]['Product']['symbol'])
    return (parse_response_data(r), r.status_code)  
  
  def request_order_change_preview(self, account_key, order_id, order_data):
    '''
    Requests an E-Trade order preview to update an already placed order. This is required before placing an updated order

    :param str account_key: your specified account key
    :param int order_id: the ID of the order you'd like to update
    :param dict order_data: a dict containing an E-Trade `PreviewOrderRequest <https://apisb.etrade.com/docs/api/order/api-order-v1.html#/definitions/PreviewOrderRequest/>`__
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/{}/change/preview.json'.format(account_key, order_id)
    headers = {'Content-Type': 'application/xml'}
    payload = xmltodict.unparse(order_data)
    r = self.session.put(url=url, headers=headers, data=payload)
    log_in_background(
      called_from = 'request_order_change_preview', 
      url = url,
      r = r,
      account_key = account_key,
      symbol = order_data['PreviewOrderRequest']['Order']['Instrument']['Product']['symbol'])
    return (parse_response_data(r), r.status_code)  

  def request_order_change_place(self, account_key, order_id, order_data):
    '''
    Places an updated order after an order preview

    :param str account_key: your specified account key
    :param int order_id: the ID of the order you'd like to update
    :param dict order_data: a dict containing an E-Trade `PlaceOrderRequest <https://apisb.etrade.com/docs/api/order/api-order-v1.html#/definitions/PlaceOrderRequest/>`__
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/{}/change/place.json'.format(account_key, order_id)
    headers = {'Content-Type': 'application/xml'}
    payload = xmltodict.unparse(order_data)
    r = self.session.put(url=url, headers=headers, data=payload)
    log_in_background(
      called_from = 'request_order_change_place', 
      url = url,
      r = r,
      account_key = account_key,
      symbol = order_data['PlaceOrderRequest']['Order'][0]['Instrument'][0]['Product']['symbol'])
    return (parse_response_data(r), r.status_code)  

  def request_order_cancel(self, account_key, order_id, symbol=''):
    '''
    Requests to cancel an already placed order

    :param str account_key: your specified account key
    :param int order_id: the ID of the order you'd like to cancel
    :param str symbol: (optional) this isn't required to cancel your order but is added to logs if provided
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/cancel.json'.format(account_key)
    headers = {'Content-Type': 'application/xml'}
    data = {'CancelOrderRequest': {'orderId': order_id}}
    payload = xmltodict.unparse(data)
    r = self.session.put(url=url, headers=headers, data=payload)
    log_in_background(
      called_from = 'request_order_cancel', 
      url = url,
      r = r,
      account_key = account_key,
      symbol = symbol)
    return (parse_response_data(r), r.status_code)  

  def request_order_detail(self, account_key, order_id, symbol=''):
    '''
    Requests detailed information for an already placed order including order status

    :param str account_key: your specified account key
    :param int order_id: the ID of your order 
    :param str symbol: (optional) this isn't required to check order status but is added to logs if provided
    '''
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/{}.json'.format(account_key, order_id)
    r = self.session.get(url=url)
    log_in_background(
      called_from = 'request_order_detail', 
      url = url,
      r = r,
      symbol = symbol)
    return (parse_response_data(r), r.status_code)