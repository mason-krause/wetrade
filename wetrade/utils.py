import logging
import pprint
import threading
import requests
import time
import traceback
import settings


def start_thread(func, name=None, args=[], kwargs={}):
  threading.Thread(target=func, name=name, args=args, kwargs=kwargs).start()

def parse_response_data(r):
  try:
    return r.json()
  except: # r.status_code == 204 (no content) and other non-parsable requests 
    return str(r.content)
  
def log_in_background(called_from, r=None, url='', tags=[], account_key='', symbol='', message='', e=None):
  start_thread(pretty_print, args=[called_from, r, url, tags, account_key, symbol, message, e])
  if settings.enable_cloud_logging == True:
    start_thread(log, args=[called_from, r, url, tags, account_key, symbol, message, e])

def pretty_print(called_from, r=None, url='', tags=[], account_key='', symbol='', message='', e=None):
  if message != '':
    print(message)
  if e:
    print('e', e)
    # traceback.print_exception(type(e), e, e.__traceback__)
  if r != None:
    response = parse_response_data(r)
    if 'Error' in response:
      response_tags = ['response', 'error']
      pprint.pprint({
        'called_from': called_from,
        'tags': [*tags, *response_tags],
        'account_key': account_key,
        'config': settings.config_id,
        'symbol': symbol,
        'url': url,
        'status_code': r.status_code, 
        'response': response})

def log(called_from, r=None, url='', tags=[], account_key='', symbol='', message='', e=None):
  if r != None:
    response = parse_response_data(r)
    log_level = 30 if 'Error' in response else 20
    response_tags = ['response'] if log_level == 20 else ['response', 'error']
    logging.log(
      log_level,
      { 'called_from': called_from,
        'tags': [*tags, *response_tags],
        'account_key': account_key,
        'config': settings.config_id,
        'symbol': symbol,
        'url': url,
        'status_code': r.status_code, 
        'response': response,
        'message': message})
  else:
    logging.info({
      'called_from': called_from,
      'tags': tags,
      'account_key': account_key,
      'config': settings.config_id,
      'symbol': symbol,
      'url': url,
      'message': message})
  if e:
    tb_info = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
    tb_str = ''.join(tb_info)
    logging.error({ 
      'called_from': called_from,
      'config': settings.config_id,
      'message': str(e),
      'tb_info': tb_str})
    
# This doesn't really belong here but E-trade doesn't have market hours endpoint
def check_market_hours(day_str=time.strftime('%Y-%m-%d', time.localtime())):
  key = settings.hours_key if hasattr(settings, 'hours_key') else 'PKNL4NZJEHKGDPLL8CVY'
  secret = settings.hours_secret if hasattr(settings, 'hours_secret') else 'sxMOohHeLG6DODKv0tu237flYuwVaM0rvoea0M2F'
  params = {'start': day_str, 'end': day_str}
  headers = {'APCA-API-KEY-ID': key, 'APCA-API-SECRET-KEY': secret}
  r = requests.get('https://paper-api.alpaca.markets/v2/calendar', params=params, headers=headers)
  results = parse_response_data(r)
  if results == []:
    return {'open': '00:00', 'close': '00:00'}
  else:
    return {'open': results[0]['open'], 'close': results[0]['close']}