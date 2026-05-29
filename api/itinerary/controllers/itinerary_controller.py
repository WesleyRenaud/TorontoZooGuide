from __future__ import annotations

from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from ..data_access.accept_itinerary import accept_itinerary
from ..data_access.clear_itinerary import clear_itinerary
from ..data_access.itinerary import fetch_itinerary_date
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_save_input_mapper import map_animal_inputs
from ..data_access.itinerary_save_input_mapper import map_named_strings
from ..data_access.itinerary_time import set_itinerary_arrival_time
from ..data_access.itinerary_time import set_itinerary_departure_time
from ...guardians.controllers.guardians_controller import GuardiansController
from ..logic import set_itinerary as set_itinerary_logic
from ..logic.itinerary import build_current_itinerary
from ..logic.itinerary_arrival_time_validation import arrival_time_is_valid_for_saved_itinerary
from ..logic.itinerary_departure_time_validation import departure_time_is_valid_for_saved_itinerary
from ..logic.itinerary_save_result import ItinerarySaveResult
from ...models import Itinerary
from ...request_connection import get_connection
from ...shared.date_values import DateValues
from ...types import DateInput, TimeInput
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController


class ItineraryController():


   @classmethod
   def get_itinerary_date( cls ) -> str | None:
      return fetch_itinerary_date( get_connection() )


   @classmethod
   def get_itinerary( cls, visit_date_temp: float | None = None ) -> Itinerary:
      return build_current_itinerary(
         saved_itinerary=fetch_saved_itinerary( get_connection() ),
         animal_controller=AnimalController,
         attraction_controller=AttractionController,
         guardians_controller=GuardiansController,
         wild_encounter_controller=WildEncounterController,
         visit_date_temp=visit_date_temp )


   @classmethod
   def set_itinerary(
         cls,
         date: DateInput,
         animals: list[ dict[ str, str ] ],
         attractions: list[ str ],
         guardians_talks: list[ dict[ str, str | None ] ],
         wild_encounters: list[ str ],
         arrival_time: TimeInput = None,
         departure_time: TimeInput = None,
         selected_exhibits: list[ str ] | None = None,
         visit_date_temp: float | None = None,
         overriding_conflicting_guardians_talks: bool = False ) -> ItinerarySaveResult:
      return set_itinerary_logic.set_itinerary(
         get_connection(),
         date=date,
         arrival_time=arrival_time,
         departure_time=departure_time,
         animals=animals,
         attractions=attractions,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         selected_exhibits=selected_exhibits,
         visit_date_temp=visit_date_temp,
         overriding_conflicting_guardians_talks=(
            overriding_conflicting_guardians_talks ),
         animal_controller=AnimalController,
         attraction_controller=AttractionController,
         guardians_controller=GuardiansController,
         wild_encounter_controller=WildEncounterController )


   @classmethod
   def clear_itinerary( cls ) -> bool:
      return clear_itinerary( get_connection() )


   @classmethod
   def set_arrival_time( cls, arrival_time: TimeInput ) -> bool:
      conn = get_connection()
      normalized_arrival_time = DateValues.normalize_itinerary_schedule_time(
         arrival_time )

      if not arrival_time_is_valid_for_saved_itinerary(
            conn,
            normalized_arrival_time ):
         return False

      return set_itinerary_arrival_time(
         conn,
         normalized_arrival_time )


   @classmethod
   def set_departure_time( cls, departure_time: TimeInput ) -> bool:
      conn = get_connection()
      normalized_departure_time = DateValues.normalize_itinerary_schedule_time(
         departure_time )

      if not departure_time_is_valid_for_saved_itinerary(
            conn,
            normalized_departure_time ):
         return False

      return set_itinerary_departure_time(
         conn,
         normalized_departure_time )


   @classmethod
   def accept_itinerary(
         cls,
         animals_to_keep: list[ dict[ str, str ] ] | None = None,
         attractions_to_keep: list[ str ] | None = None ) -> bool:
      return accept_itinerary(
         get_connection(),
         animals_to_keep=list( map_animal_inputs( animals_to_keep ) ),
         attractions_to_keep=list( map_named_strings( attractions_to_keep ) ) )
