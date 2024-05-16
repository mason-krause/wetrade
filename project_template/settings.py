# Google Cloud settings (optional)
# need GOOGLE_APPLICATION_CREDENTIALS env var set to json path
enable_cloud_logging = False
quote_bucket = 'your-quote-bucket'
# E-trade settings
login_method = 'auto' # 'auto', 'manual'
use_2fa = False # needed to disable SMS auth - requires totp_secret
config_id = 'prod'
config_options = {
    'sandbox':{
      'base_url': 'https://apisb.etrade.com/',
      'client_key': 'SANDBOX_CLIENT_KEY',
      'client_secret': 'SANDBOX_CLIENT_SECRET',
      'username': 'USERNAME',
      'password': 'PASSWORD',
      'totp_secret': 'TOTP_SECRET'},
    'prod':{
      'base_url': 'https://api.etrade.com/',
      'client_key': 'PROD_CLIENT_KEY',
      'client_secret': 'PROD_CLIENT_SECRET',
      'username': 'USERNAME',
      'password': 'PASSWORD',
      'totp_secret': 'TOTP_SECRET'}}

config = config_options[config_id]