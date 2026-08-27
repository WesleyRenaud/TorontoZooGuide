from __future__ import annotations

from typing import Any

from ...animal_item_key import AnimalScheduleItemKey
from ...attraction_item_key import AttractionScheduleItemKey
from ...data_access.attraction_also_transportation_provider import AttractionAlsoTransportationProvider
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from .listed_schedule_item_persistence import commit_listed_schedule
from .listed_schedule_item_persistence import prepare_schedule_item_on_itinerary
from .listed_schedule_target import resolve_listed_schedule_target
from .parse_schedule_time_options import ParsedScheduleTimeOptions
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.walk_node_id_for_transportation import walk_node_id_for_transportation
from .schedule_item_key import ListedScheduleItemKey
from .schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from .schedule_itinerary_helpers import build_save_result
from .schedule_itinerary_helpers import effective_duration_seconds
from .schedule_itinerary_helpers import prepare_schedule_window
from .schedule_itinerary_helpers import resolve_slot_times_allowing_visit_extension
from ....shared.enums import ItineraryErrorType
from ....types import Connection
from ...warnings.itinerary_suppressed_warnings_builder import ItinerarySuppressedWarningsBuilder
from ...warnings.schedule_item_not_on_itinerary_warning_builder import ScheduleItemNotOnItineraryWarningBuilder


def schedule_listed_itinerary_item(
      conn: Connection,
      schedule_item_key: ListedScheduleItemKey,
      time_options: ParsedScheduleTimeOptions,
      *,
      itinerary_context: dict[ str, Any ],
      confirming_schedule_item_not_on_itinerary: bool,
      ) -> ItinerarySaveResult:
   saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
   prepared_window = prepare_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_context )

   if isinstance( prepared_window, ItinerarySaveResult ):
      return prepared_window

   suppressed_warnings, membership_error = prepare_schedule_item_on_itinerary(
      conn,
      saved_itinerary,
      schedule_item_key,
      itinerary_context=itinerary_context,
      confirming_schedule_item_not_on_itinerary=(
         confirming_schedule_item_not_on_itinerary
      ) )

   if membership_error is not None:
      return membership_error

   if SavedItineraryScheduleItemRowFinder.saved_schedule_item_is_already_scheduled(
         saved_itinerary,
         schedule_item_key ):
      return ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
         build_save_result(
            conn,
            ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
            **itinerary_context ),
         suppressed_warnings )

   target = resolve_listed_schedule_target( conn, schedule_item_key )

   duration_seconds = effective_duration_seconds(
      time_options.duration_minutes,
      target.default_duration_seconds )

   if duration_seconds is None:
      return build_save_result(
         conn,
         ItineraryErrorType.SAVE_FAILED,
         **itinerary_context )

   candidate_walk_node_id = _walk_node_id_for_listed_item(
      conn,
      schedule_item_key )
   visit_anchor_seconds = prepared_window.window[ 0 ]
   earliest_start_seconds = ScheduleItemTravelTimeCalculator.earliest_schedule_start_seconds_with_travel(
      saved_itinerary,
      candidate_walk_node_id=candidate_walk_node_id,
      visit_anchor_seconds=visit_anchor_seconds,
      itinerary_context=itinerary_context,
      start_time=time_options.start_time )

   slot, slot_error = resolve_slot_times_allowing_visit_extension(
      conn,
      saved_itinerary,
      prepared_window.window,
      duration_seconds,
      start_time=time_options.start_time,
      itinerary_context=itinerary_context,
      earliest_start_seconds=earliest_start_seconds )

   if slot_error is not None:
      return slot_error

   start_time_key, end_time = slot

   return ItinerarySuppressedWarningsBuilder.with_suppressed_warnings(
      commit_listed_schedule(
         conn,
         schedule_item_key=schedule_item_key,
         start_time=start_time_key,
         end_time=end_time,
         insert_if_missing=not ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
            saved_itinerary,
            schedule_item_key ),
         itinerary_context=itinerary_context ),
      suppressed_warnings )


def _walk_node_id_for_listed_item(
      conn: Connection,
      schedule_item_key: ListedScheduleItemKey ) -> str | None:
   if isinstance( schedule_item_key, AnimalScheduleItemKey ):
      return ScheduleItemTravelTimeCalculator.walk_node_id_for_animal(
         species=schedule_item_key.species,
         exhibit=schedule_item_key.exhibit,
         enclosure_name=schedule_item_key.enclosure_name )

   if isinstance( schedule_item_key, AttractionScheduleItemKey ):
      if AttractionAlsoTransportationProvider.attraction_is_also_transportation(
            conn,
            schedule_item_key.name ):
         return walk_node_id_for_transportation( schedule_item_key.name )

      return ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction( schedule_item_key.name )

   return None
