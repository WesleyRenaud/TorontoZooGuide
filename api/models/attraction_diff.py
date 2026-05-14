class AttractionDiff:
   def __init__( self, name, old_likelihood, new_likelihood ):
      self.name = name
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood


   def to_dict( self ):
      return {
         'name': self.name,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
      }
