from __future__ import annotations

from ..animal_item_key import format_animal_schedule_item_key
from .itinerary_stop import ENTRANCE_ITEM_KEY
from .itinerary_stop import ItineraryStop
from ...models import Itinerary
from ...shared.calendar_dates import DateValues
from ...shared.enums import ScheduleItemKind
from ...types import ScheduleTimeKey
from ...walk_graph.data_access.load_walk_graph import load_walk_graph
from ...walk_graph.domain.map_location_kind import MapLocationKind
from ...walk_graph.domain.map_location_walk_node import MapLocationWalkNode
from ...walk_graph.domain.walk_graph import WalkGraph
from ...walk_graph.domain.walk_graph_node import WalkGraphNode
from ...walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from ...walk_graph.resolve_viewing_walk_node_id import resolve_viewing_walk_node_id


def resolve_entrance_itinerary_stop() -> ItineraryStop:
   walk_graph = load_walk_graph()
   entrance_node = _walk_graph_node_by_id(
      walk_graph,
      walk_graph[ 'entrance_node_id' ] )

   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.ENTRANCE,
      item_key=ENTRANCE_ITEM_KEY,
      walk_node_ids=[ entrance_node[ 'id' ] ],
      x_coord=entrance_node[ 'x' ],
      y_coord=entrance_node[ 'y' ] )


def resolve_itinerary_stops( itinerary: Itinerary ) -> list[ ItineraryStop ]:
   stops: list[ ItineraryStop ] = [ resolve_entrance_itinerary_stop() ]

   for animal in itinerary.animals:
      if animal.covered_by_talk:
         continue

      walk_node_id = resolve_viewing_walk_node_id(
         animal.species,
         animal.exhibit,
         animal.x_coord,
         animal.y_coord,
         animal.enclosure_name )
      walk_node_ids = [ walk_node_id ] if walk_node_id != None else []

      stops.append(
         ItineraryStop(
            schedule_item_kind=ScheduleItemKind.ANIMAL,
            item_key=format_animal_schedule_item_key(
               animal.species,
               animal.exhibit,
               animal.enclosure_name ),
            walk_node_ids=walk_node_ids,
            x_coord=animal.x_coord,
            y_coord=animal.y_coord,
            is_fixed_time=_has_schedule_times( animal.start_time, animal.end_time ),
            start_time=animal.start_time,
            end_time=animal.end_time ) )

   for attraction in itinerary.attractions:
      map_location = walk_node_for_map_location(
         MapLocationKind.ATTRACTION,
         attraction.name )

      stops.append(
         _stop_from_map_location(
            schedule_item_kind=ScheduleItemKind.ATTRACTION,
            item_key=attraction.name,
            map_location=map_location,
            x_coord=attraction.x_coord,
            y_coord=attraction.y_coord,
            start_time=attraction.start_time,
            end_time=attraction.end_time ) )

   for transportation in itinerary.transportations:
      # Also-attraction transportations share the attraction map-location name.
      map_location = walk_node_for_map_location(
         MapLocationKind.ATTRACTION,
         transportation.name )

      stops.append(
         _stop_from_map_location(
            schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
            item_key=transportation.name,
            map_location=map_location,
            x_coord=transportation.x_coord,
            y_coord=transportation.y_coord,
            start_time=transportation.start_time,
            end_time=transportation.end_time ) )

   for guardians_talk in itinerary.guardians_talks:
      if guardians_talk.is_deleted:
         continue

      map_location = walk_node_for_map_location(
         MapLocationKind.GUARDIANS_TALK,
         guardians_talk.name,
         location=guardians_talk.location )

      stops.append(
         _stop_from_map_location(
            schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
            item_key=guardians_talk.name,
            map_location=map_location,
            x_coord=guardians_talk.x_coord,
            y_coord=guardians_talk.y_coord,
            start_time=guardians_talk.start_time,
            end_time=guardians_talk.end_time ) )

   for wild_encounter in itinerary.wild_encounters:
      if wild_encounter.is_deleted:
         continue

      map_location = walk_node_for_map_location(
         MapLocationKind.WILD_ENCOUNTER_MEETING_SPOT,
         wild_encounter.meeting_spot )

      stops.append(
         _stop_from_map_location(
            schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
            item_key=wild_encounter.name,
            meeting_spot=wild_encounter.meeting_spot,
            map_location=map_location,
            x_coord=wild_encounter.x_coord,
            y_coord=wild_encounter.y_coord,
            start_time=wild_encounter.start_time,
            end_time=wild_encounter.end_time ) )

   return stops


def resolve_fixed_time_itinerary_stops(
      itinerary: Itinerary ) -> list[ ItineraryStop ]:
   return [
      stop
      for stop in resolve_itinerary_stops( itinerary )
      if stop.is_fixed_time
   ]


def _stop_from_map_location(
      *,
      schedule_item_kind: ScheduleItemKind,
      item_key: str,
      map_location: MapLocationWalkNode | None,
      meeting_spot: str | None = None,
      x_coord: float | None,
      y_coord: float | None,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> ItineraryStop:
   walk_node_ids: list[ str ] = []

   if map_location is not None:
      walk_node_ids = [ map_location.walk_node_id ]

   return ItineraryStop(
      schedule_item_kind=schedule_item_kind,
      item_key=item_key,
      meeting_spot=meeting_spot,
      walk_node_ids=walk_node_ids,
      x_coord=x_coord,
      y_coord=y_coord,
      is_fixed_time=_has_schedule_times( start_time, end_time ),
      start_time=start_time,
      end_time=end_time )


def _has_schedule_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> bool:
   return bool(
      DateValues.normalize_schedule_time_key( start_time )
      and DateValues.normalize_schedule_time_key( end_time ) )


def _walk_graph_node_by_id(
      walk_graph: WalkGraph,
      node_id: str ) -> WalkGraphNode:
   for node in walk_graph[ 'nodes' ]:
      if node[ 'id' ] == node_id:
         return node

   raise ValueError( 'Walk graph node %r not found' % ( node_id, ) )
