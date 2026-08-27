from __future__ import annotations

from typing import Any

from .bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from .bulk_schedule_start_state import BulkScheduleStartState
from .bulk_schedule_walk_order_builder import BulkScheduleWalkOrderBuilder
from .bulk_schedule_window_prep import BulkScheduleWindowPrep
from ..core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.saved_itinerary import SavedItinerary
from ...domain.itinerary_builder import ItineraryBuilder
from ..items.prepared_schedule_window import PreparedScheduleWindow
from ...routing.partition_itinerary_schedule_windows import partition_itinerary_schedule_windows
from ...routing.resolve_itinerary_stops import resolve_fixed_time_itinerary_stops
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ..unscheduling.itinerary_schedule_clearer import ItineraryScheduleClearer
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.walk_graph import WalkGraph
from ....zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider


class BulkScheduleWindowPreparer():
   @classmethod
   def has_items_to_rebuild(
         cls,
         saved_itinerary: SavedItinerary ) -> bool:
      return bool(
         saved_itinerary.animal_rows
         or saved_itinerary.attraction_rows
         or saved_itinerary.transportation_rows
         or saved_itinerary.guardians_talk_rows
         or saved_itinerary.wild_encounter_rows )


   @classmethod
   def start_state(
         cls,
         walk_graph: WalkGraph,
         animal_rows: list[ ItineraryAnimalRecord ],
         anchor_seconds: int ) -> BulkScheduleStartState:
      entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
      scheduled_rows = [
         animal_row
         for animal_row in animal_rows
         if GuestItemScheduleStatusChecker.has_schedule_times(
            animal_row.start_time,
            animal_row.end_time )
      ]

      if not scheduled_rows:
         return BulkScheduleStartState(
            start_node_id=entrance_node_id,
            schedule_anchor_seconds=anchor_seconds )

      last_scheduled_row = max(
         scheduled_rows,
         key=lambda animal_row: DateValues.time_value_in_seconds(
            animal_row.end_time ) or -1 )

      start_node_id = BulkScheduleWalkOrderBuilder.representative_walk_node_id(
         walk_graph,
         entrance_node_id,
         last_scheduled_row.species,
         last_scheduled_row.exhibit,
         last_scheduled_row.enclosure_name ) or entrance_node_id
      last_end_seconds = DateValues.time_value_in_seconds(
         last_scheduled_row.end_time ) or anchor_seconds

      return BulkScheduleStartState(
         start_node_id=start_node_id,
         schedule_anchor_seconds=max( anchor_seconds, last_end_seconds ) )


   @classmethod
   def prepare_windows(
         cls,
         conn: Connection,
         *,
         prepared_window: PreparedScheduleWindow,
         itinerary_context: dict[ str, Any ] ) -> BulkScheduleWindowPrep:
      previous_itinerary = ItineraryBuilder.build_current(
         prepared_window.saved_itinerary,
         **itinerary_context )

      ItineraryScheduleClearer.clear_all( conn )

      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      anchor_seconds, day_end_seconds = prepared_window.window
      itinerary = ItineraryBuilder.build_current(
         saved_itinerary,
         **itinerary_context )
      blockers = TimeBlockBuilder.collect_from_itinerary( itinerary )
      walk_graph = load_walk_graph()
      start_state = cls.start_state(
         walk_graph,
         saved_itinerary.animal_rows,
         anchor_seconds )
      fixed_time_stops = resolve_fixed_time_itinerary_stops( itinerary )
      boundary_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
         conn,
         itinerary,
         fixed_time_stops )
      schedule_windows = partition_itinerary_schedule_windows(
         start_state.schedule_anchor_seconds,
         day_end_seconds,
         boundary_stops )
      loop_pins = BulkScheduleLoopPinAttacher.keep_completable( schedule_windows, loop_pins )
      visit_date = ItineraryProvider.fetch_itinerary_date( conn )
      zoo_hours_record = (
         None
         if visit_date is None
         else ZooHoursProvider.fetch_zoo_hours_record( conn, visit_date ) )
      zoo_operating_hours = (
         None
         if zoo_hours_record is None
         else zoo_hours_record.operating_hours() )

      return BulkScheduleWindowPrep(
         saved_itinerary=saved_itinerary,
         previous_itinerary=previous_itinerary,
         itinerary_context=itinerary_context,
         anchor_seconds=anchor_seconds,
         day_end_seconds=day_end_seconds,
         blockers=blockers,
         walk_graph=walk_graph,
         start_state=start_state,
         schedule_windows=schedule_windows,
         loop_pins=loop_pins,
         visit_date=visit_date,
         zoo_operating_hours=zoo_operating_hours )
