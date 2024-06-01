import logging
import pprint
import threading
import requests
import time
import traceback
import os
import ast
import google.cloud.logging
from google.cloud import secretmanager
try: 
  import settings
except ModuleNotFoundError:
  import wetrade.project_template.settings as settings


def start_thread(func, name=None, args=[], kwargs={}):
  threading.Thread(target=func, name=name, args=args, kwargs=kwargs).start()

def parse_response_data(r):
  try:
    return r.json()
  except: # r.status_code == 204 (no content) and other non-parsable requests 
    return str(r.content)
  
def log_in_background(called_from, r=None, url='', tags=[], account_key='', symbol='', message='', e=None):
  start_thread(pretty_print, args=[called_from, r, url, tags, account_key, symbol, message, e])
  if hasattr(settings, 'enable_logging') and settings.enable_logging == True:
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

def setup_cloud_logging():
  if hasattr(settings, 'enable_logging') and settings.enable_logging == True:
    client = google.cloud.logging.Client()
    client.setup_logging()

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
  
def get_gcloud_secret(secret_id, version_id='latest'):
  gcloud_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '!no-gcloud-file!')
  if gcloud_file != '!no-gcloud-file!':
    with open(gcloud_file) as f:
      data = f.read()
    gcloud_data = ast.literal_eval(data)
    project_id = gcloud_data['project_id']
    secret_name = f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    return response.payload.data.decode('UTF-8')