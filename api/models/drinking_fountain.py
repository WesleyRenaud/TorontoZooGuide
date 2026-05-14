from ..zoo_util import ZooUtil


class DrinkingFountain:
   def __init__(
         self,
         x_coord,
         y_coord,
         is_closed=False,
         closed_message=None,
         likelihood=None ):
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood
      }
