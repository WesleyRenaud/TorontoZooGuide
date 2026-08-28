from __future__ import annotations

from collections.abc import Callable
from copy import copy
from datetime import date
from typing import Any

from ....animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from .attraction_animal_coverer import AttractionAnimalCoverer
from .attraction_animal_coverer import CoveredAnimalAttraction
from .bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from .bulk_schedule_stop_selector import BulkScheduleStopSelector
from .bulk_schedule_window_preparer import BulkScheduleWindowPreparer
from ..core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...data_access.saved_itinerary import SavedItinerary
from ...data_access.validated_itinerary import ValidatedItinerary
from ...domain.itinerary_builder import ItineraryBuilder
from .guardians_talk_animal_coverer import CoveredAnimalTalk
from .guardians_talk_animal_coverer import GuardiansTalkAnimalCoverer
from ..items.schedule_window_preparer import ScheduleWindowPreparer
from .loop_schedule_slot import LoopScheduleSlot
from .loop_schedule_slot_sink import LoopScheduleSlotSink
from .loop_schedule_unit_builder import LoopScheduleUnitBuilder
from .master_route_loop_animal_grouper import MasterRouteLoopAnimalGrouper
from .master_route_loop_scheduler import MasterRouteLoopScheduler
from ....models import Itinerary
from ...results.itinerary_result_reason import ItineraryResultReason
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.itinerary_schedule_window_partitioner import ItineraryScheduleWindowPartitioner
from ...routing.itinerary_stop_resolver import ItineraryStopResolver
from ....shared.enums import ItineraryErrorType
from ....shared.enums import ItinerarySaveIssueItemType
from ....types import Types
from ....walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from ....walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey
from ...warnings.fixed_time_item_long_wait_warning_builder import FixedTimeItemLongWaitWarningBuilder

class BulkRescheduleLongWaitSimulator():
   @classmethod
   def is_isolated_after_adding(
         cls,
         conn: Types.Connection,
         new_item: Any,
         *,
         propose_on_itinerary: Callable[
            [ Itinerary, Any, dict[ str, Any ] ],
            Itinerary | None,
         ],
         itinerary_context: dict[ str, Any ] ) -> bool:
      """True when scheduling new_item leaves it isolated even after packing animals."""
      saved_itinerary = ItineraryProvider.fetch_saved_itinerary( conn )
      current_itinerary = ItineraryBuilder.build_current(
         saved_itinerary,
         **itinerary_context )

      if not FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding( current_itinerary, new_item ):
         return False

      animals_to_schedule = BulkScheduleStopSelector.animals(
         saved_itinerary,
         only_previously_scheduled=True )

      if not animals_to_schedule:
         return True

      proposed_itinerary = propose_on_itinerary(
         current_itinerary,
         new_item,
         itinerary_context )

      if proposed_itinerary is None:
         return True

      packed_itinerary = cls.pack_animals_in_memory(
         conn,
         proposed_itinerary,
         animals_to_schedule=animals_to_schedule,
         itinerary_context=itinerary_context )

      if packed_itinerary is None:
         return True

      new_item_block = TimeBlockBuilder.from_schedule_times(
         new_item.start_time,
         new_item.end_time )

      if new_item_block is None:
         return False

      return FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated_on_schedule(
         new_item_block,
         TimeBlockBuilder.collect_from_itinerary( packed_itinerary ) )


   @classmethod
   def newly_added_reason(
         cls,
         conn: Types.Connection,
         validated_itinerary: ValidatedItinerary,
         *,
         visit_date: date,
         itinerary_context: dict[ str, Any ],
         saved_itinerary: SavedItinerary | None = None,
         ) -> ItineraryResultReason | None:
      if not any(
            cls._has_newly_added_isolated_fixed_time_items(
               validated_itinerary,
               item_type,
               saved_itinerary=saved_itinerary )
            for item_type in FixedTimeItemLongWaitWarningBuilder.LONG_WAIT_ITEM_TYPES
      ):
         return None

      animals_with_times = [
         animal
         for animal in validated_itinerary.animals
         if GuestItemScheduleStatusChecker.has_schedule_times( animal.start_time, animal.end_time )
      ]
      packed_itinerary: Itinerary | None = None

      if animals_with_times:
         animals_to_schedule = [
            ItineraryAnimalRecord(
               species=animal.species,
               exhibit=animal.exhibit,
               enclosure_name=animal.enclosure_name,
               old_likelihood=animal.old_likelihood,
               new_likelihood=animal.new_likelihood,
               is_added=animal.is_added,
               covered_by_talk=animal.covered_by_talk,
               start_time=animal.start_time,
               end_time=animal.end_time )
            for animal in animals_with_times
         ]
         proposed_itinerary = cls._build_itinerary_from_proposed_items(
            validated_itinerary,
            visit_date=visit_date,
            itinerary_context=itinerary_context )
         packed_itinerary = cls.pack_animals_in_memory(
            conn,
            proposed_itinerary,
            animals_to_schedule=animals_to_schedule,
            itinerary_context=itinerary_context )

      issue_items = []

      for item_type in FixedTimeItemLongWaitWarningBuilder.LONG_WAIT_ITEM_TYPES:
         for item in cls._newly_added_long_wait_items_for_type(
               validated_itinerary,
               item_type,
               packed_itinerary=packed_itinerary,
               saved_itinerary=saved_itinerary ):
            issue_items.append(
               FixedTimeItemLongWaitWarningBuilder.build_issue_item( item_type, item ) )

      if not issue_items:
         return None

      return ItineraryResultReason(
         code=ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items=issue_items )


   @classmethod
   def _has_newly_added_isolated_fixed_time_items(
         cls,
         validated_itinerary: ValidatedItinerary,
         item_type: ItinerarySaveIssueItemType,
         *,
         saved_itinerary: SavedItinerary | None ) -> bool:
      isolated_items = FixedTimeItemLongWaitWarningBuilder.isolated_from_validated_itinerary(
         validated_itinerary,
         item_type )

      if saved_itinerary is None:
         return bool( isolated_items )

      return bool(
         FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
            saved_itinerary,
            isolated_items,
            item_type ) )


   @classmethod
   def _newly_added_long_wait_items_for_type(
         cls,
         validated_itinerary: ValidatedItinerary,
         item_type: ItinerarySaveIssueItemType,
         *,
         packed_itinerary: Itinerary | None,
         saved_itinerary: SavedItinerary | None ) -> list[ Any ]:
      if packed_itinerary is None:
         isolated_items = FixedTimeItemLongWaitWarningBuilder.isolated_from_validated_itinerary(
            validated_itinerary,
            item_type )
      else:
         isolated_after_pack = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
            packed_itinerary,
            item_type )
         isolated_names = { item.name for item in isolated_after_pack }
         isolated_items = [
            item
            for item in FixedTimeItemLongWaitWarningBuilder.items_from_validated(
               validated_itinerary,
               item_type )
            if not item.is_deleted and item.name in isolated_names
         ]

      if saved_itinerary is None:
         return isolated_items

      return FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
         saved_itinerary,
         isolated_items,
         item_type )


   @classmethod
   def pack_animals_in_memory(
         cls,
         conn: Types.Connection,
         itinerary: Itinerary,
         *,
         animals_to_schedule: list[ ItineraryAnimalRecord ],
         itinerary_context: dict[ str, Any ] ) -> Itinerary | None:
      if not animals_to_schedule:
         return itinerary

      prepared_window = ScheduleWindowPreparer.prepare_zoo_hours(
         conn,
         ItineraryProvider.fetch_saved_itinerary( conn ),
         **itinerary_context )

      if isinstance( prepared_window, ItinerarySaveResult ):
         return None

      anchor_seconds, day_end_seconds = prepared_window.window
      packing_itinerary = cls._itinerary_with_cleared_animal_times( itinerary )
      blockers = TimeBlockBuilder.collect_from_itinerary( packing_itinerary )
      walk_graph = WalkGraphProvider.fetch()
      start_state = BulkScheduleWindowPreparer.start_state(
         walk_graph,
         [],
         anchor_seconds )
      fixed_time_stops = ItineraryStopResolver.resolve_fixed_time( packing_itinerary )
      boundary_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
         conn,
         packing_itinerary,
         fixed_time_stops )
      schedule_windows = ItineraryScheduleWindowPartitioner.partition(
         start_state.schedule_anchor_seconds,
         day_end_seconds,
         boundary_stops )
      loop_pins = BulkScheduleLoopPinAttacher.keep_completable( schedule_windows, loop_pins )
      covered_by_talk = GuardiansTalkAnimalCoverer.keys_to_cover(
         conn,
         loop_pins,
         animals_to_schedule )
      covered_by_attraction = AttractionAnimalCoverer.keys_to_cover(
         conn,
         [
            attraction.name
            for attraction in packing_itinerary.attractions
         ],
         animals_to_schedule )
      covered_keys = AttractionAnimalCoverer.merge_keys(
         covered_by_talk,
         covered_by_attraction )
      animals_to_pack = GuardiansTalkAnimalCoverer.excluding_covered(
         animals_to_schedule,
         covered_keys )
      sorted_loop_groups = MasterRouteLoopAnimalGrouper.group( animals_to_pack )
      loop_units = LoopScheduleUnitBuilder.build( sorted_loop_groups )
      schedule_windows = BulkScheduleLoopPinAttacher.attach_to_windows(
         schedule_windows,
         loop_pins )

      if loop_units:
         slot_sink = LoopScheduleSlotSink( persist=False )
         MasterRouteLoopScheduler.schedule(
            conn,
            loop_units,
            blockers=blockers,
            schedule_windows=schedule_windows,
            schedule_cursor_seconds=start_state.schedule_anchor_seconds,
            walk_graph=walk_graph,
            start_node_id=start_state.start_node_id,
            slot_sink=slot_sink )
         cls._apply_slots_to_itinerary_animals( packing_itinerary, slot_sink.slots )

      cls._apply_talk_covered_to_itinerary_animals( packing_itinerary, covered_by_talk )
      cls._apply_attraction_covered_to_itinerary_animals(
         packing_itinerary,
         covered_by_attraction )

      return packing_itinerary


   @classmethod
   def _itinerary_with_cleared_animal_times( cls, itinerary: Itinerary ) -> Itinerary:
      cleared_animals = []

      for animal in itinerary.animals:
         cleared_animal = copy( animal )
         cleared_animal.start_time = None
         cleared_animal.end_time = None
         cleared_animal.covered_by_talk = False
         cleared_animals.append( cleared_animal )

      cleared_attractions = []

      for attraction in itinerary.attractions:
         cleared_attraction = copy( attraction )
         cleared_attraction.start_time = None
         cleared_attraction.end_time = None
         cleared_attractions.append( cleared_attraction )

      return ItineraryBuilder.build(
         date=itinerary.date,
         selected_exhibits=list( itinerary.selected_exhibits ),
         animals=cleared_animals,
         attractions=cleared_attractions,
         transportations=list( itinerary.transportations ),
         transportation_stations=list( itinerary.transportation_stations ),
         guardians_talks=list( itinerary.guardians_talks ),
         wild_encounters=list( itinerary.wild_encounters ),
         events=list( itinerary.events ),
         arrival_time=itinerary.arrival_time,
         departure_time=itinerary.departure_time )


   @classmethod
   def _build_itinerary_from_proposed_items(
         cls,
         proposed: ValidatedItinerary,
         *,
         visit_date: date,
         itinerary_context: dict[ str, Any ] ) -> Itinerary:
      animal_rows = [
         ItineraryAnimalRecord(
            species=animal.species,
            exhibit=animal.exhibit,
            enclosure_name=animal.enclosure_name,
            old_likelihood=animal.old_likelihood,
            new_likelihood=animal.new_likelihood,
            is_added=animal.is_added,
            covered_by_talk=animal.covered_by_talk,
            start_time=animal.start_time,
            end_time=animal.end_time )
         for animal in proposed.animals
      ]
      attraction_rows = [
         ItineraryAttractionRecord(
            attraction=attraction.name,
            old_likelihood=attraction.old_likelihood,
            new_likelihood=attraction.new_likelihood,
            start_time=attraction.start_time,
            end_time=attraction.end_time )
         for attraction in proposed.attractions
      ]
      talk_rows = [
         ItineraryGuardiansTalkRecord(
            talk_name=talk.name,
            start_time=talk.start_time,
            end_time=talk.end_time,
            is_deleted=talk.is_deleted )
         for talk in proposed.guardians_talks
      ]
      encounter_rows = [
         ItineraryWildEncounterRecord(
            wild_encounter=encounter.name,
            start_time=encounter.start_time,
            end_time=encounter.end_time,
            is_deleted=encounter.is_deleted )
         for encounter in proposed.wild_encounters
      ]
      animals = itinerary_context[ 'animal_coordinator' ].get_animals_for_saved_itinerary(
         day=visit_date.day,
         month=visit_date.month,
         year=visit_date.year,
         saved_animals=animal_rows,
         temp=itinerary_context.get( 'visit_date_temp' ) )
      attractions = itinerary_context[
         'attraction_coordinator'
      ].get_attractions_for_saved_itinerary(
         day=visit_date.day,
         month=visit_date.month,
         year=visit_date.year,
         saved_attractions=attraction_rows )
      guardians_talks = itinerary_context[
         'guardians_coordinator'
      ].get_guardians_talks_for_saved_itinerary( talk_rows )
      wild_encounters = itinerary_context[
         'wild_encounter_coordinator'
      ].get_wild_encounters_for_saved_itinerary( encounter_rows )

      return ItineraryBuilder.build(
         date=visit_date,
         selected_exhibits=[],
         animals=animals,
         attractions=attractions,
         transportations=[],
         transportation_stations=[],
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         events=list( proposed.events ),
         arrival_time=proposed.arrival_time,
         departure_time=proposed.departure_time )


   @classmethod
   def _apply_slots_to_itinerary_animals(
         cls,
         itinerary: Itinerary,
         slots: list[ LoopScheduleSlot ] ) -> None:
      animals_by_spot = {
         ViewingSpotKeyBuilder.from_animal( animal ): animal
         for animal in itinerary.animals
      }
      attractions_by_name = {
         attraction.name: attraction
         for attraction in itinerary.attractions
      }

      for stop, start_time, end_time in slots:
         if isinstance( stop, ItineraryAttractionRecord ):
            attraction = attractions_by_name.get( stop.attraction )

            if attraction is None:
               continue

            attraction.start_time = start_time
            attraction.end_time = end_time
            continue

         animal = animals_by_spot.get(
            ViewingSpotKeyBuilder.from_values(
               stop.species,
               stop.exhibit,
               stop.enclosure_name ) )

         if animal is None:
            continue

         animal.start_time = start_time
         animal.end_time = end_time


   @classmethod
   def _apply_talk_covered_to_itinerary_animals(
         cls,
         itinerary: Itinerary,
         covered_by_talk: dict[ ViewingSpotNameKey, CoveredAnimalTalk ],
      ) -> None:
      animals_by_spot = {
         ViewingSpotKeyBuilder.from_animal( animal ): animal
         for animal in itinerary.animals
      }

      for animal_row, loop_pin in covered_by_talk.values():
         animal = animals_by_spot.get( animal_row.viewing_spot_key() )

         if animal is None:
            continue

         animal.start_time = loop_pin.stop.start_time
         animal.end_time = loop_pin.stop.end_time
         animal.covered_by_talk = True


   @classmethod
   def _apply_attraction_covered_to_itinerary_animals(
         cls,
         itinerary: Itinerary,
         covered_by_attraction: dict[ ViewingSpotNameKey, CoveredAnimalAttraction ],
      ) -> None:
      animals_by_spot = {
         ViewingSpotKeyBuilder.from_animal( animal ): animal
         for animal in itinerary.animals
      }
      attraction_by_name = {
         attraction.name: attraction
         for attraction in itinerary.attractions
      }

      for animal_row, attraction_name in covered_by_attraction.values():
         animal = animals_by_spot.get( animal_row.viewing_spot_key() )
         attraction = attraction_by_name.get( attraction_name )

         if animal is None or attraction is None:
            continue

         if attraction.start_time is None or attraction.end_time is None:
            continue

         animal.start_time = attraction.start_time
         animal.end_time = attraction.end_time
         animal.covered_by_talk = True
