from ..zoo_util import ZooUtil


class Restroom:
   def __init__(
         self,
         title,
         x_coord=None,
         y_coord=None,
         is_closed=None,
         closed_message=None,
         has_alert=None,
         alert_message=None ):
      self.title = title
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.has_alert = has_alert
      self.alert_message = alert_message


   def to_dict( self ):
      return {
         'title': self.title,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'has_alert': ZooUtil.as_boolean( self.has_alert ),
         'alert_message': self.alert_message
      }
