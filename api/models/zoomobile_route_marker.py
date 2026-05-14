class ZoomobileRouteMarker:
   def __init__( self, route_type, x_coord, y_coord ):
      self.route_type = route_type
      self.x_coord = x_coord
      self.y_coord = y_coord


   def to_dict( self ):
      return {
         'route_type': self.route_type,
         'x_coord': self.x_coord,
         'y_coord': self.y_coord
      }
