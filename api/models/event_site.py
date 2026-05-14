class EventSite:
   def __init__( self, name, x_coord, y_coord ):
      self.name = name
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
