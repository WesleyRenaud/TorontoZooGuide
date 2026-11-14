from __future__ import annotations


class AnimalViewingAlert:
   species: str
   exhibit: str
   start_date: str | None
   end_date: str | None
   message: str


   def __init__(
         self,
         species: str,
         exhibit: str,
         start_date: str | None,
         end_date: str | None,
         message: str ) -> None:
      self.species = species
      self.exhibit = exhibit
      self.start_date = start_date
      self.end_date = end_date
      self.message = message
