from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .parse_schedule_item_request import parse_schedule_item_request
from .parse_schedule_time_options import parse_schedule_time_options
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_guardians_talk_itinerary_item import schedule_guardians_talk_itinerary_item
from .schedule_itinerary_event import schedule_itinerary_event
from .schedule_itinerary_helpers import build_itinerary_context
from .schedule_itinerary_helpers import build_save_result
from .schedule_listed_itinerary_item import schedule_listed_itinerary_item
from .schedule_wild_encounter_itinerary_item import schedule_wild_encounter_itinerary_item
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ScheduleItemKind
from ....types import Connection
from ....types import DurationInput
from ....types import TimeInput
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


def schedule_itinerary_item(
      conn: Connection,
      item_type: str,
      key: str,
      *,
      start_time: TimeInput = None,
      duration_minutes: DurationInput = None,
      animal_coordinator: type[ AnimalCoordinator ],
      attraction_coordinator: type[ AttractionCoordinator ],
      guardians_coordinator: type[ GuardiansCoordinator ],
      wild_encounter_coordinator: type[ WildEncounterCoordinator ],
      confirming_schedule_item_not_on_itinerary: bool,
      confirming_guardians_talk_unschedule: bool,
      confirming_wild_encounter_unschedule: bool ) -> ItinerarySaveResult:
   itinerary_context = build_itinerary_context(
      animal_coordinator=animal_coordinator,
      attraction_coordinator=attraction_coordinator,
      guardians_coordinator=guardians_coordinator,
      wild_encounter_coordinator=wild_encounter_coordinator )

   parsed = parse_schedule_item_request( item_type, key )

   if parsed is None:
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

   if parsed.kind == ScheduleItemKind.EVENT:
      return schedule_itinerary_event(
         conn,
         event_type=parsed.event_type,
         time_options=parsed_schedule_options,
         itinerary_context=itinerary_context )

   if parsed.kind == ScheduleItemKind.GUARDIANS_TALK:
      return schedule_guardians_talk_itinerary_item(
         conn,
         parsed.talk_name or '',
         itinerary_context=itinerary_context,
         confirming_guardians_talk_unschedule=(
            confirming_guardians_talk_unschedule ) )

   if parsed.kind == ScheduleItemKind.WILD_ENCOUNTER:
      return schedule_wild_encounter_itinerary_item(
         conn,
         parsed.wild_encounter_name or '',
         itinerary_context=itinerary_context,
         confirming_wild_encounter_unschedule=(
            confirming_wild_encounter_unschedule ) )

   return schedule_listed_itinerary_item(
      conn,
      parsed,
      parsed_schedule_options,
      itinerary_context=itinerary_context,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ) )
