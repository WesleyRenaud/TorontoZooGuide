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
from ..logic import remove_itinerary_item as remove_itinerary_item_logic
from ..logic import schedule_itinerary_item as schedule_itinerary_item_logic
from ..logic import set_itinerary as set_itinerary_logic
from ..logic import unschedule_itinerary_item as unschedule_itinerary_item_logic
from ..logic.itinerary import build_current_itinerary
from ..logic.itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from ..logic.itinerary_departure_time_validation import departure_time_is_valid_for_zoo_hours
from ..logic.itinerary_save_result import ItinerarySaveResult
from ..logic.itinerary_time_set_result import ItineraryTimeSetResult
from ..logic.short_visit_warning import apply_short_visit_warning_preferences
from ..logic.short_visit_warning import short_visit_warning_is_required
from ...models import Itinerary
from ...request_connection import get_connection
from ...shared.date_values import DateValues
from ...shared.enums import ItineraryErrorType
from ...types import DateInput, DurationInput, TimeInput
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from ...zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record


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
         overriding_conflicting_guardians_talks: bool = False,
         confirming_short_visit: bool = False,
         suppress_short_visit_warning: bool = False,
         confirming_guardians_talk_unschedule: bool = False ) -> ItinerarySaveResult:
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
         confirming_short_visit=confirming_short_visit,
         suppress_short_visit_warning=suppress_short_visit_warning,
         confirming_guardians_talk_unschedule=confirming_guardians_talk_unschedule,
         animal_controller=AnimalController,
         attraction_controller=AttractionController,
         guardians_controller=GuardiansController,
         wild_encounter_controller=WildEncounterController )


   @classmethod
   def schedule_itinerary_item(
         cls,
         item_type: str,
         key: str,
         *,
         start_time: TimeInput = None,
         duration_minutes: DurationInput = None,
         confirming_schedule_item_not_on_itinerary: bool = False,
         suppress_schedule_item_not_on_itinerary_warning: bool = False,
         confirming_guardians_talk_unschedule: bool = False ) -> ItinerarySaveResult:
      return schedule_itinerary_item_logic.schedule_itinerary_item(
         get_connection(),
         item_type,
         key,
         start_time=start_time,
         duration_minutes=duration_minutes,
         animal_controller=AnimalController,
         attraction_controller=AttractionController,
         guardians_controller=GuardiansController,
         wild_encounter_controller=WildEncounterController,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ),
         suppress_schedule_item_not_on_itinerary_warning=(
            suppress_schedule_item_not_on_itinerary_warning
         ),
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule
         ) )


   @classmethod
   def clear_itinerary( cls ) -> bool:
      return clear_itinerary( get_connection() )


   @classmethod
   def unschedule_itinerary_item(
         cls,
         item_type: str,
         key: str ) -> ItinerarySaveResult:
      return unschedule_itinerary_item_logic.unschedule_itinerary_item(
         get_connection(),
         item_type,
         key )


   @classmethod
   def remove_itinerary_item(
         cls,
         item_type: str,
         key: str ) -> ItinerarySaveResult:
      return remove_itinerary_item_logic.remove_itinerary_item(
         get_connection(),
         item_type,
         key )


   @classmethod
   def set_arrival_time(
         cls,
         arrival_time: TimeInput,
         *,
         confirming_short_visit: bool = False,
         suppress_short_visit_warning: bool = False ) -> ItineraryTimeSetResult:
      conn = get_connection()
      normalized_arrival_time = DateValues.normalize_itinerary_schedule_time(
         arrival_time )

      if normalized_arrival_time is None:
         set_itinerary_arrival_time( conn, None )
         return ItineraryTimeSetResult()

      saved_itinerary = fetch_saved_itinerary( conn )
      zoo_hours_record = fetch_zoo_hours_record(
         conn,
         fetch_itinerary_date( conn ) )

      validation_error = arrival_time_is_valid_for_zoo_hours(
         normalized_arrival_time,
         zoo_hours_record,
         departure_time=saved_itinerary.departure_time )

      if validation_error != ItineraryErrorType.SUCCESS:
         return ItineraryTimeSetResult( error_type=validation_error )

      if short_visit_warning_is_required(
            conn,
            normalized_arrival_time,
            saved_itinerary.departure_time,
            confirming_short_visit=confirming_short_visit ):
         return ItineraryTimeSetResult(
            error_type=ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

      apply_short_visit_warning_preferences(
         conn,
         suppress_short_visit_warning=suppress_short_visit_warning )

      set_itinerary_arrival_time( conn, normalized_arrival_time )

      return ItineraryTimeSetResult()


   @classmethod
   def set_departure_time(
         cls,
         departure_time: TimeInput,
         *,
         confirming_short_visit: bool = False,
         suppress_short_visit_warning: bool = False ) -> ItineraryTimeSetResult:
      conn = get_connection()
      normalized_departure_time = DateValues.normalize_itinerary_schedule_time(
         departure_time )

      if normalized_departure_time is None:
         set_itinerary_departure_time( conn, None )
         return ItineraryTimeSetResult()

      saved_itinerary = fetch_saved_itinerary( conn )
      zoo_hours_record = fetch_zoo_hours_record(
         conn,
         fetch_itinerary_date( conn ) )

      validation_error = departure_time_is_valid_for_zoo_hours(
         normalized_departure_time,
         zoo_hours_record,
         arrival_time=saved_itinerary.arrival_time )

      if validation_error != ItineraryErrorType.SUCCESS:
         return ItineraryTimeSetResult( error_type=validation_error )

      if short_visit_warning_is_required(
            conn,
            saved_itinerary.arrival_time,
            normalized_departure_time,
            confirming_short_visit=confirming_short_visit ):
         return ItineraryTimeSetResult(
            error_type=ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

      apply_short_visit_warning_preferences(
         conn,
         suppress_short_visit_warning=suppress_short_visit_warning )

      set_itinerary_departure_time( conn, normalized_departure_time )

      return ItineraryTimeSetResult()


   @classmethod
   def accept_itinerary(
         cls,
         animals_to_keep: list[ dict[ str, str ] ] | None = None,
         attractions_to_keep: list[ str ] | None = None ) -> bool:
      return accept_itinerary(
         get_connection(),
         animals_to_keep=list( map_animal_inputs( animals_to_keep ) ),
         attractions_to_keep=list( map_named_strings( attractions_to_keep ) ) )
