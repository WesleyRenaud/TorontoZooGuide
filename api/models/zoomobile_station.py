class ZoomobileStation:
   def __init__( self, name, description=None, x_coord=None, y_coord=None ):
      self.name = name
      self.description = description
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'name': self.name,
         'description': self.description,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
