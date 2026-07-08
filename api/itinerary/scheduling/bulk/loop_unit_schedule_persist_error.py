from __future__ import annotations

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord


class LoopUnitSchedulePersistError( Exception ):
   def __init__( self, animals: list[ ItineraryAnimalRecord ] ) -> None:
      self.animals = animals
      super().__init__()
