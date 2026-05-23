from __future__ import annotations


class AnimalDiff:
   def __init__(
         self,
         species: str,
         exhibit: str,
         old_likelihood: int | None,
         new_likelihood: int | None ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'species': self.species,
         'exhibit': self.exhibit,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
      }
