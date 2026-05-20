class RegionWithExhibits:
   def __init__( self, name, exhibits ):
      self.name = name
      self.exhibits = exhibits or []


   def to_dict( self ):
      return {
         'name': self.name,
         'exhibits': self.exhibits,
      }
