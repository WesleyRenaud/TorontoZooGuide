from __future__ import annotations

from dataclasses import dataclass

from ..core.time_block import earliest_scheduled_start_seconds
from ..core.time_block import latest_scheduled_end_seconds
from ...data_access.saved_itinerary import SavedItinerary
from ...domain.itinerary import build_current_itinerary
from ....models import Itinerary
from ...routing.walk_node_id_for_transportation import walk_node_id_for_transportation
from ...routing.walk_travel_time import travel_time_seconds_between_nodes
from ....shared.calendar_dates import DateValues
from ....types import ScheduleTimeKey
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.map_location_kind import MapLocationKind
from ....walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from ....walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot


@dataclass( frozen=True )
class _ScheduledWalkStop:
   start_seconds: int
   end_seconds: int
   walk_node_id: str


def earliest_schedule_start_seconds_with_travel(
      saved_itinerary: SavedItinerary,
      *,
      candidate_walk_node_id: str | None,
      visit_anchor_seconds: int,
      itinerary_context: dict,
      start_time: ScheduleTimeKey | None = None ) -> int:
   if candidate_walk_node_id is None:
      return visit_anchor_seconds

   walk_graph = load_walk_graph()
   previous_end_seconds, previous_node_id = (
      _previous_stop_end_and_walk_node(
         saved_itinerary,
         visit_anchor_seconds=visit_anchor_seconds,
         itinerary_context=itinerary_context,
         before_start_seconds=(
            DateValues.time_value_in_seconds( start_time )
            if start_time is not None
            else None ) ) )

   travel_seconds = travel_time_seconds_between_nodes(
      walk_graph,
      previous_node_id,
      candidate_walk_node_id )

   return max(
      visit_anchor_seconds,
      previous_end_seconds + travel_seconds )


def entrance_travel_seconds_to_earliest_item( itinerary: Itinerary ) -> int:
   walk_node_id = walk_node_id_for_earliest_scheduled_item( itinerary )

   if walk_node_id is None:
      return 0

   walk_graph = load_walk_graph()

   return travel_time_seconds_between_nodes(
      walk_graph,
      str( walk_graph[ 'entrance_node_id' ] ),
      walk_node_id )


def entrance_travel_seconds_from_latest_item( itinerary: Itinerary ) -> int:
   walk_node_id = walk_node_id_for_latest_scheduled_item( itinerary )

   if walk_node_id is None:
      return 0

   walk_graph = load_walk_graph()

   return travel_time_seconds_between_nodes(
      walk_graph,
      walk_node_id,
      str( walk_graph[ 'entrance_node_id' ] ) )


def walk_node_id_for_animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None ) -> str | None:
   return walk_node_id_for_viewing_spot(
      species,
      exhibit,
      enclosure_name )


def walk_node_id_for_attraction( attraction_name: str ) -> str | None:
   walk_node = walk_node_for_map_location(
      MapLocationKind.ATTRACTION,
      attraction_name )

   if walk_node is None:
      return None

   return walk_node.walk_node_id


def walk_node_id_for_earliest_scheduled_item(
      itinerary: Itinerary ) -> str | None:
   earliest_start_seconds = earliest_scheduled_start_seconds( itinerary )

   if earliest_start_seconds is None:
      return None

   for stop in _scheduled_stops_with_walk_nodes( itinerary ):
      if stop.start_seconds == earliest_start_seconds:
         return stop.walk_node_id

   return None


def walk_node_id_for_latest_scheduled_item(
      itinerary: Itinerary ) -> str | None:
   latest_end_seconds = latest_scheduled_end_seconds( itinerary )

   if latest_end_seconds is None:
      return None

   for stop in _scheduled_stops_with_walk_nodes( itinerary ):
      if stop.end_seconds == latest_end_seconds:
         return stop.walk_node_id

   return None


def _scheduled_stops_with_walk_nodes(
      itinerary: Itinerary ) -> list[ _ScheduledWalkStop ]:
   stops: list[ _ScheduledWalkStop ] = []

   for animal in itinerary.animals:
      if animal.covered_by_talk:
         continue

      _append_scheduled_stop_with_walk_node(
         stops,
         start_time=animal.start_time,
         end_time=animal.end_time,
         walk_node_id=walk_node_id_for_animal(
            species=animal.species,
            exhibit=animal.exhibit,
            enclosure_name=animal.enclosure_name ) )

   for attraction in itinerary.attractions:
      _append_scheduled_stop_with_walk_node(
         stops,
         start_time=attraction.start_time,
         end_time=attraction.end_time,
         walk_node_id=walk_node_id_for_attraction( attraction.name ) )

   for transportation in itinerary.transportations:
      _append_scheduled_stop_with_walk_node(
         stops,
         start_time=transportation.start_time,
         end_time=transportation.end_time,
         walk_node_id=walk_node_id_for_transportation(
            transportation.name,
            legs=transportation.legs ) )

   for talk in itinerary.guardians_talks:
      if talk.is_deleted:
         continue

      walk_node = walk_node_for_map_location(
         MapLocationKind.GUARDIANS_TALK,
         talk.name )

      _append_scheduled_stop_with_walk_node(
         stops,
         start_time=talk.start_time,
         end_time=talk.end_time,
         walk_node_id=(
            None if walk_node is None else walk_node.walk_node_id ) )

   for encounter in itinerary.wild_encounters:
      if encounter.is_deleted:
         continue

      walk_node = walk_node_for_map_location(
         MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
         encounter.meeting_spot )

      _append_scheduled_stop_with_walk_node(
         stops,
         start_time=encounter.start_time,
         end_time=encounter.end_time,
         walk_node_id=(
            None if walk_node is None else walk_node.walk_node_id ) )

   return stops


def _append_scheduled_stop_with_walk_node(
      stops: list[ _ScheduledWalkStop ],
      *,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
      walk_node_id: str | None ) -> None:
   start_seconds = DateValues.time_value_in_seconds( start_time )
   end_seconds = DateValues.time_value_in_seconds( end_time )

   if start_seconds is None or end_seconds is None or walk_node_id is None:
      return

   stops.append(
      _ScheduledWalkStop(
         start_seconds=start_seconds,
         end_seconds=end_seconds,
         walk_node_id=walk_node_id ) )


def _previous_stop_end_and_walk_node(
      saved_itinerary: SavedItinerary,
      *,
      visit_anchor_seconds: int,
      itinerary_context: dict,
      before_start_seconds: int | None ) -> tuple[ int, str ]:
   walk_graph = load_walk_graph()
   entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
   itinerary = build_current_itinerary( saved_itinerary, **itinerary_context )
   previous_candidates: list[ tuple[ int, str ] ] = [
      ( visit_anchor_seconds, entrance_node_id ),
   ]

   for stop in _scheduled_stops_with_walk_nodes( itinerary ):
      if (
            before_start_seconds is not None
            and stop.end_seconds > before_start_seconds ):
         continue

      previous_candidates.append( ( stop.end_seconds, stop.walk_node_id ) )

   return max( previous_candidates, key=lambda item: item[ 0 ] )
