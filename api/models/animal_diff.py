from __future__ import annotations


class AnimalDiff:
   def __init__(
         self,
         species: str,
         exhibit: str,
         old_likelihood: int | None,
         new_likelihood: int | None,
         is_added: bool = False ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood
      self.is_added = is_added


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'species': self.species,
         'exhibit': self.exhibit,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
         'is_added': self.is_added,
      }
