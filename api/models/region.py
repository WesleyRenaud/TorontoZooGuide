class Region:
   def __init__( self, name, has_exhibits ):
      self.name = name
      self.has_exhibits = has_exhibits


   def to_dict( self ):
      return {
         'name': self.name,
         'hasExhibits': self.has_exhibits,
      }
