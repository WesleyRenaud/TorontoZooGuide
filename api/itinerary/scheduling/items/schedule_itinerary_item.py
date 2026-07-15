from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from ...guardians_talk_item_key import GuardiansTalkScheduleItemKey
from .parse_schedule_time_options import parse_schedule_time_options
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_guardians_talk_itinerary_item import schedule_guardians_talk_itinerary_item
from .schedule_item_key import ScheduleItemKey
from .schedule_itinerary_event import schedule_itinerary_event
from .schedule_itinerary_helpers import build_itinerary_context
from .schedule_itinerary_helpers import build_save_result
from .schedule_listed_itinerary_item import schedule_listed_itinerary_item
from .schedule_wild_encounter_itinerary_item import schedule_wild_encounter_itinerary_item
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ItineraryEventType
from ....types import Connection
from ....types import DurationInput
from ....types import TimeInput
from ...wild_encounter_item_key import WildEncounterScheduleItemKey
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def schedule_itinerary_item(
      conn: Connection,
      schedule_item_key: ScheduleItemKey | None,
      *,
      start_time: TimeInput = None,
      duration_minutes: DurationInput = None,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      confirming_schedule_item_not_on_itinerary: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool,
      confirming_fixed_time_item_long_wait: bool,
      confirming_guardians_talk_without_animal: bool ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator )

   if schedule_item_key is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   parsed_schedule_options = parse_schedule_time_options(
      start_time,
      duration_minutes )

   if isinstance( parsed_schedule_options, ItineraryErrorType ):
      return build_save_result(
         conn,
         parsed_schedule_options,
         **itinerary_context )

   if isinstance( schedule_item_key, ItineraryEventType ):
      return schedule_itinerary_event(
         conn,
         event_type=schedule_item_key,
         time_options=parsed_schedule_options,
         itinerary_context=itinerary_context )

   if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
      return schedule_guardians_talk_itinerary_item(
         conn,
         schedule_item_key,
         itinerary_context=itinerary_context,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ),
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ),
         confirming_guardians_talk_without_animal=(
            confirming_guardians_talk_without_animal ) )

   if isinstance( schedule_item_key, WildEncounterScheduleItemKey ):
      return schedule_wild_encounter_itinerary_item(
         conn,
         schedule_item_key,
         itinerary_context=itinerary_context,
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ),
         confirming_fixed_time_item_long_wait=(
            confirming_fixed_time_item_long_wait ) )

   return schedule_listed_itinerary_item(
      conn,
      schedule_item_key,
      parsed_schedule_options,
      itinerary_context=itinerary_context,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ) )
