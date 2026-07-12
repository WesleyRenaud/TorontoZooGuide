from __future__ import annotations

from copy import copy
from datetime import date
from typing import Any

from ....animals.search.animals_matching_query import viewing_spot_key
from ....animals.search.animals_matching_query import viewing_spot_key_from_values
from .animals_for_bulk_schedule import animals_for_bulk_schedule
from .bulk_schedule_animals import has_itinerary_schedule_times
from .bulk_schedule_loop_pins import attach_loop_pins_to_schedule_windows
from .bulk_schedule_loop_pins import keep_completable_loop_pins
from .bulk_schedule_loop_pins import separate_schedule_boundaries_and_loop_pins
from .bulk_schedule_start_state import BulkScheduleStartState
from ..core.time_block import collect_time_blocks_from_itinerary
from ...data_access.itinerary import fetch_saved_itinerary
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from ...data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...data_access.validated_itinerary import ValidatedItinerary
from ...domain.itinerary import build_current_itinerary
from ...domain.itinerary import build_itinerary
from .group_animals_by_master_route_loop import group_animals_by_master_route_loop
from ..items.schedule_itinerary_helpers import prepare_zoo_hours_schedule_window
from .loop_schedule_unit import build_loop_schedule_units
from .loop_unit_schedule_slots import LoopScheduleSlot
from .loop_unit_schedule_slots import LoopScheduleSlotSink
from ....models import GuardiansTalk
from ....models import Itinerary
from ....models.guardians_talk_diff import GuardiansTalkDiff
from ...results.itinerary_save_result import ItinerarySaveResult
from ...routing.partition_itinerary_schedule_windows import partition_itinerary_schedule_windows
from ...routing.resolve_itinerary_stops import resolve_fixed_time_itinerary_stops
from .schedule_animals_by_master_route_loop import schedule_animals_by_master_route_loop
from ....types import Connection
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.walk_graph import WalkGraph
from ...warnings.guardians_talk_long_wait_warning import isolated_guardians_talks_after_adding_talk
from ...warnings.guardians_talk_long_wait_warning import isolated_guardians_talks_from_itinerary
from ...warnings.guardians_talk_long_wait_warning import isolated_guardians_talks_from_validated_itinerary


def isolated_guardians_talks_after_adding_talk_with_simulated_bulk(
      conn: Connection,
      new_talk: GuardiansTalkDiff,
      *,
      itinerary_context: dict[ str, Any ] ) -> list[ GuardiansTalkDiff ]:
   saved_itinerary = fetch_saved_itinerary( conn )
   current_itinerary = build_current_itinerary(
      saved_itinerary,
      **itinerary_context )
   currently_isolated = isolated_guardians_talks_after_adding_talk(
      current_itinerary,
      new_talk )

   if not currently_isolated:
      return []

   animals_to_schedule = animals_for_bulk_schedule(
      saved_itinerary,
      only_previously_scheduled=True )

   if not animals_to_schedule:
      return currently_isolated

   proposed_itinerary = _itinerary_with_proposed_talk(
      current_itinerary,
      new_talk,
      itinerary_context[ 'guardians_coordinator' ] )

   if proposed_itinerary is None:
      return currently_isolated

   packed_itinerary = pack_animals_into_itinerary_in_memory(
      conn,
      proposed_itinerary,
      animals_to_schedule=animals_to_schedule,
      itinerary_context=itinerary_context )

   if packed_itinerary is None:
      return currently_isolated

   isolated_after_pack = isolated_guardians_talks_from_itinerary( packed_itinerary )
   isolated_names = { talk.name for talk in isolated_after_pack }

   if new_talk.name in isolated_names:
      return [ new_talk ]

   return []


def isolated_guardians_talks_after_simulated_bulk_for_validated_itinerary(
      conn: Connection,
      validated_itinerary: ValidatedItinerary,
      *,
      visit_date: date,
      itinerary_context: dict[ str, Any ] ) -> list[ GuardiansTalkDiff ]:
   animals_with_times = [
      animal
      for animal in validated_itinerary.animals
      if has_itinerary_schedule_times( animal.start_time, animal.end_time )
   ]

   if not animals_with_times:
      return isolated_guardians_talks_from_validated_itinerary(
         validated_itinerary )

   animals_to_schedule = [
      ItineraryAnimalRecord(
         species=animal.species,
         exhibit=animal.exhibit,
         enclosure_name=animal.enclosure_name,
         old_likelihood=animal.old_likelihood,
         new_likelihood=animal.new_likelihood,
         is_added=animal.is_added,
         start_time=animal.start_time,
         end_time=animal.end_time )
      for animal in animals_with_times
   ]
   proposed_itinerary = _build_itinerary_from_proposed_items(
      validated_itinerary,
      visit_date=visit_date,
      itinerary_context=itinerary_context )
   packed_itinerary = pack_animals_into_itinerary_in_memory(
      conn,
      proposed_itinerary,
      animals_to_schedule=animals_to_schedule,
      itinerary_context=itinerary_context )

   if packed_itinerary is None:
      return isolated_guardians_talks_from_validated_itinerary(
         validated_itinerary )

   isolated_after_pack = isolated_guardians_talks_from_itinerary( packed_itinerary )
   isolated_names = { talk.name for talk in isolated_after_pack }

   return [
      talk
      for talk in validated_itinerary.guardians_talks
      if not talk.is_deleted and talk.name in isolated_names
   ]


def pack_animals_into_itinerary_in_memory(
      conn: Connection,
      itinerary: Itinerary,
      *,
      animals_to_schedule: list[ ItineraryAnimalRecord ],
      itinerary_context: dict[ str, Any ] ) -> Itinerary | None:
   if not animals_to_schedule:
      return itinerary

   schedule_window = prepare_zoo_hours_schedule_window(
      conn,
      fetch_saved_itinerary( conn ),
      **itinerary_context )

   if isinstance( schedule_window, ItinerarySaveResult ):
      return None

   _, ( anchor_seconds, day_end_seconds ) = schedule_window
   packing_itinerary = _itinerary_with_cleared_animal_times( itinerary )
   blockers = collect_time_blocks_from_itinerary( packing_itinerary )
   walk_graph = load_walk_graph()
   start_state = _bulk_schedule_start_state_for_unscheduled_animals(
      walk_graph,
      anchor_seconds )
   sorted_loop_groups = group_animals_by_master_route_loop( animals_to_schedule )
   loop_units = build_loop_schedule_units( sorted_loop_groups )
   fixed_time_stops = resolve_fixed_time_itinerary_stops( packing_itinerary )
   boundary_stops, loop_pins = separate_schedule_boundaries_and_loop_pins(
      conn,
      packing_itinerary,
      fixed_time_stops )
   schedule_windows = partition_itinerary_schedule_windows(
      start_state.schedule_anchor_seconds,
      day_end_seconds,
      boundary_stops )
   loop_pins = keep_completable_loop_pins( schedule_windows, loop_pins )
   schedule_windows = attach_loop_pins_to_schedule_windows(
      schedule_windows,
      loop_pins )

   if not loop_units:
      return packing_itinerary

   slot_sink = LoopScheduleSlotSink( persist=False )
   schedule_animals_by_master_route_loop(
      conn,
      loop_units,
      blockers=blockers,
      schedule_windows=schedule_windows,
      schedule_cursor_seconds=start_state.schedule_anchor_seconds,
      walk_graph=walk_graph,
      start_node_id=start_state.start_node_id,
      slot_sink=slot_sink )
   _apply_slots_to_itinerary_animals( packing_itinerary, slot_sink.slots )

   return packing_itinerary


def _bulk_schedule_start_state_for_unscheduled_animals(
      walk_graph: WalkGraph,
      anchor_seconds: int ) -> BulkScheduleStartState:
   return BulkScheduleStartState(
      start_node_id=str( walk_graph[ 'entrance_node_id' ] ),
      schedule_anchor_seconds=anchor_seconds )


def _itinerary_with_cleared_animal_times( itinerary: Itinerary ) -> Itinerary:
   cleared_animals = []

   for animal in itinerary.animals:
      cleared_animal = copy( animal )
      cleared_animal.start_time = None
      cleared_animal.end_time = None
      cleared_animals.append( cleared_animal )

   return build_itinerary(
      date=itinerary.date,
      animals=cleared_animals,
      attractions=list( itinerary.attractions ),
      guardians_talks=list( itinerary.guardians_talks ),
      wild_encounters=list( itinerary.wild_encounters ),
      events=list( itinerary.events ),
      arrival_time=itinerary.arrival_time,
      departure_time=itinerary.departure_time )


def _itinerary_with_proposed_talk(
      itinerary: Itinerary,
      new_talk: GuardiansTalkDiff,
      guardians_coordinator: Any ) -> Itinerary | None:
   talk_details = guardians_coordinator.get_guardians_talk_details(
      [ new_talk.name ] )

   if not talk_details:
      return None

   detail = talk_details[ 0 ]
   proposed_talk = GuardiansTalk(
      name=new_talk.name,
      location=new_talk.location or detail.location,
      x_coord=detail.x_coord,
      y_coord=detail.y_coord,
      maximum_duration=detail.maximum_duration,
      start_time=new_talk.start_time,
      end_time=new_talk.end_time,
      is_deleted=new_talk.is_deleted )
   talks = [
      talk
      for talk in itinerary.guardians_talks
      if talk.name != new_talk.name
   ]
   talks.append( proposed_talk )

   return build_itinerary(
      date=itinerary.date,
      animals=list( itinerary.animals ),
      attractions=list( itinerary.attractions ),
      guardians_talks=talks,
      wild_encounters=list( itinerary.wild_encounters ),
      events=list( itinerary.events ),
      arrival_time=itinerary.arrival_time,
      departure_time=itinerary.departure_time )


def _build_itinerary_from_proposed_items(
      proposed: ValidatedItinerary,
      *,
      visit_date: date,
      itinerary_context: dict[ str, Any ] ) -> Itinerary:
   from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord

   animal_rows = [
      ItineraryAnimalRecord(
         species=animal.species,
         exhibit=animal.exhibit,
         enclosure_name=animal.enclosure_name,
         old_likelihood=animal.old_likelihood,
         new_likelihood=animal.new_likelihood,
         is_added=animal.is_added,
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

   return build_itinerary(
      date=visit_date,
      animals=animals,
      attractions=attractions,
      guardians_talks=guardians_talks,
      wild_encounters=wild_encounters,
      events=list( proposed.events ),
      arrival_time=proposed.arrival_time,
      departure_time=proposed.departure_time )


def _apply_slots_to_itinerary_animals(
      itinerary: Itinerary,
      slots: list[ LoopScheduleSlot ] ) -> None:
   animals_by_spot = {
      viewing_spot_key( animal ): animal
      for animal in itinerary.animals
   }

   for animal_row, start_time, end_time in slots:
      animal = animals_by_spot.get(
         viewing_spot_key_from_values(
            animal_row.species,
            animal_row.exhibit,
            animal_row.enclosure_name ) )

      if animal is None:
         continue

      animal.start_time = start_time
      animal.end_time = end_time
