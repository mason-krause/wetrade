import xmltodict
from wetrade.utils import parse_response_data, log_in_background
from wetrade.user_session import UserSession


class APIClient:
  def __init__(self, session=None):
    self.session = UserSession() if session==None else session

  def request_account_list(self):
    url = self.session.config['base_url'] + 'v1/accounts/list.json'
    r = self.session.get(url=url)
    log_in_background(
      called_from = 'request_account_list', 
      url = url,
      r = r)
    return (parse_response_data(r), r.status_code)

  def request_account_balance(self, account_key):
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
    url = self.session.config['base_url'] + 'v1/accounts/{}/portfolio.json'.format(account_key)
    r = self.session.get(url=url)
    log_in_background(
      called_from = 'request_account_portfolio', 
      url = url,
      r = r,
      account_key = account_key)
    return (parse_response_data(r), r.status_code)
  
  def request_account_orders(self, account_key, start_date='', end_date='', marker=''):
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

  def request_order_status(self, account_key, order_id, symbol=''):
    url = self.session.config['base_url'] + 'v1/accounts/{}/orders/{}.json'.format(account_key, order_id)
    r = self.session.get(url=url)
    log_in_background(
      called_from = 'request_order_status', 
      url = url,
      r = r,
      symbol = symbol)
    return (parse_response_data(r), r.status_code)