from __future__ import annotations


class AttractionDiff:
   def __init__(
         self,
         name: str,
         old_likelihood: int | None,
         new_likelihood: int | None ) -> None:
      self.name = name
      self.old_likelihood = old_likelihood
      self.new_likelihood = new_likelihood


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'name': self.name,
         'old_likelihood': self.old_likelihood,
         'new_likelihood': self.new_likelihood,
      }
