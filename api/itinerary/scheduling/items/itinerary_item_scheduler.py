from __future__ import annotations

from ....animals.coordinators.animal_coordinator import AnimalCoordinator
from .attraction_itinerary_item_scheduler import AttractionItineraryItemScheduler
from ...attraction_schedule_item_key import AttractionScheduleItemKey
from ....attractions.coordinators.attraction_coordinator import AttractionCoordinator
from ....guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from .guardians_talk_itinerary_item_scheduler import GuardiansTalkItineraryItemScheduler
from ...guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from .itinerary_event_scheduler import ItineraryEventScheduler
from .itinerary_save_result_builder import ItinerarySaveResultBuilder
from .itinerary_schedule_context_builder import ItineraryScheduleContextBuilder
from .listed_itinerary_item_scheduler import ListedItineraryItemScheduler
from ...results.itinerary_save_result import ItinerarySaveResult
from .schedule_item_key import ScheduleItemKey
from .schedule_time_options_parser import ScheduleTimeOptionsParser
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ItineraryEventType
from ....types import Types
from .wild_encounter_itinerary_item_scheduler import WildEncounterItineraryItemScheduler
from ...wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from ....wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


class ItineraryItemScheduler():
   @classmethod
   def schedule(
         cls,
         conn: Types.Connection,
         schedule_item_key: ScheduleItemKey.Key | None,
         *,
         start_time: Types.TimeInput = None,
         duration_minutes: Types.DurationInput = None,
         animal_coordinator: type[ AnimalCoordinator ],
         attraction_coordinator: type[ AttractionCoordinator ],
         guardians_coordinator: type[ GuardiansCoordinator ],
         wild_encounter_coordinator: type[ WildEncounterCoordinator ],
         confirming_schedule_item_not_on_itinerary: bool,
         confirming_attraction_outside_operating_hours: bool,
         confirming_guardians_talk_unschedule: bool,
         confirming_wild_encounter_unschedule: bool,
         confirming_fixed_time_item_long_wait: bool,
         confirming_guardians_talk_without_animal: bool ) -> ItinerarySaveResult:
      itinerary_context = ItineraryScheduleContextBuilder.build(
         animal_coordinator=animal_coordinator,
         attraction_coordinator=attraction_coordinator,
         guardians_coordinator=guardians_coordinator,
         wild_encounter_coordinator=wild_encounter_coordinator )

      if schedule_item_key is None:
         return ItinerarySaveResultBuilder.save_result(
            conn,
            ItineraryErrorType.SAVE_FAILED,
            **itinerary_context )

      parsed_schedule_options = ScheduleTimeOptionsParser.parse(
         start_time,
         duration_minutes )

      if isinstance( parsed_schedule_options, ItineraryErrorType ):
         return ItinerarySaveResultBuilder.save_result(
            conn,
            parsed_schedule_options,
            **itinerary_context )

      if isinstance( schedule_item_key, ItineraryEventType ):
         return ItineraryEventScheduler.schedule(
            conn,
            event_type=schedule_item_key,
            time_options=parsed_schedule_options,
            itinerary_context=itinerary_context )

      if isinstance( schedule_item_key, GuardiansTalkScheduleItemKey ):
         return GuardiansTalkItineraryItemScheduler.schedule(
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
         return WildEncounterItineraryItemScheduler.schedule(
            conn,
            schedule_item_key,
            itinerary_context=itinerary_context,
            confirming_wild_encounter_unschedule=(
               confirming_wild_encounter_unschedule ),
            confirming_fixed_time_item_long_wait=(
               confirming_fixed_time_item_long_wait ) )

      if isinstance( schedule_item_key, AttractionScheduleItemKey ):
         return AttractionItineraryItemScheduler.schedule(
            conn,
            schedule_item_key,
            parsed_schedule_options,
            itinerary_context=itinerary_context,
            confirming_schedule_item_not_on_itinerary=(
               confirming_schedule_item_not_on_itinerary
            ),
            confirming_attraction_outside_operating_hours=(
               confirming_attraction_outside_operating_hours
            ) )

      return ListedItineraryItemScheduler.schedule(
         conn,
         schedule_item_key,
         parsed_schedule_options,
         itinerary_context=itinerary_context,
         confirming_schedule_item_not_on_itinerary=(
            confirming_schedule_item_not_on_itinerary
         ) )
