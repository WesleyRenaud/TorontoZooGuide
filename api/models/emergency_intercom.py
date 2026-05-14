class EmergencyIntercom:
   def __init__( self, x_coord, y_coord ):
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
