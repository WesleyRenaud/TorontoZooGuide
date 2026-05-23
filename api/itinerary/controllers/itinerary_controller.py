from __future__ import annotations

from ... import zoo
from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ...guardians.controllers.guardians_controller import GuardiansController
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...types import DateInput
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.accept_itinerary import accept_itinerary
from ..data_access.clear_itinerary import clear_itinerary
from ..logic import set_itinerary as set_itinerary_logic
from ..logic.itinerary import build_current_itinerary
from ...request_connection import get_connection


class ItineraryController():


   @classmethod
   def get_itinerary( cls ) -> zoo.Itinerary:
      return build_current_itinerary(
         saved_itinerary=fetch_saved_itinerary( get_connection() ),
         animal_controller=AnimalController,
         attraction_controller=AttractionController,
         guardians_controller=GuardiansController,
         wild_encounter_controller=WildEncounterController )


   @classmethod
   def set_itinerary(
         cls,
         date: DateInput,
         animals: list[ dict[ str, str ] ],
         attractions: list[ str ],
         guardians_talks: list[ str ],
         wild_encounters: list[ str ] ) -> bool:
      return set_itinerary_logic.set_itinerary(
         get_connection(),
         date=date,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         animal_controller=AnimalController,
         attraction_controller=AttractionController,
         guardians_controller=GuardiansController,
         wild_encounter_controller=WildEncounterController )


   @classmethod
   def clear_itinerary( cls ) -> bool:
      return clear_itinerary( get_connection() )


   @classmethod
   def accept_itinerary( cls ) -> bool:
      return accept_itinerary( get_connection() )
