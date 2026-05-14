class AnimalDiff:
   def __init__( self, species, exhibit, old_likelihood, new_likelihood ):
      self.species = species
      self.exhibit = exhibit
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood


   def to_dict( self ):
      return {
         'species': self.species,
         'exhibit': self.exhibit,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
      }
