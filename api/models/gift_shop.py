from ..zoo_util import ZooUtil


class GiftShop:
   def __init__( self, name, location, description=None, x_coord=None, y_coord=None, is_closed=None, closed_message=None,
                 likelihood=None ):
      self.name = name
      self.location = location
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord
      self.is_closed = is_closed
      self.closed_message = closed_message
      self.likelihood = likelihood


   def to_dict( self ):
      return {
         'name': self.name,
         'location': self.location,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord,
         'is_closed': ZooUtil.as_boolean( self.is_closed ),
         'closed_message': self.closed_message,
         'likelihood': self.likelihood,
      }
