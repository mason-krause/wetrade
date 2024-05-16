from . import BaseOrder

class LimitOrder(BaseOrder):
  def __init__(self, *args, **kwargs):
    self.order_type = 'LIMIT'
    BaseOrder.__init__(self, *args, **kwargs)
    
class StopOrder(BaseOrder):
  def __init__(self, *args, **kwargs):
    self.order_type = 'STOP'
    BaseOrder.__init__(self, *args, **kwargs)
    
class MarketOrder(BaseOrder):
  def __init__(self, *args, **kwargs):
    self.order_type = 'MARKET'
    BaseOrder.__init__(self, *args, **kwargs)
    
class StopLimitOrder(BaseOrder):
  def __init__(self, *args, **kwargs):
    self.order_type = 'STOP_LIMIT'
    BaseOrder.__init__(self, *args, **kwargs)