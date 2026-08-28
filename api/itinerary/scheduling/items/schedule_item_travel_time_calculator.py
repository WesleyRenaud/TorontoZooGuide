from __future__ import annotations

from ..core.time_block_builder import TimeBlockBuilder
from ...data_access.saved_itinerary import SavedItinerary
from ...domain.itinerary_builder import ItineraryBuilder
from ....models import Itinerary
from ...routing.transit_ride_endpoint import TransitRideEndpoint
from ...routing.transportation_walk_node_resolver import TransportationWalkNodeResolver
from ...routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from .scheduled_walk_stop import ScheduledWalkStop
from ....shared.calendar_dates import DateValues
from ....types import ScheduleTimeKey
from ....walk_graph.data_access.load_walk_graph import load_walk_graph
from ....walk_graph.domain.map_location_kind import MapLocationKind
from ....walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from ....walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver


class ScheduleItemTravelTimeCalculator():
   @classmethod
   def earliest_schedule_start_seconds_with_travel(
         cls,
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
         cls._previous_stop_end_and_walk_node(
            saved_itinerary,
            visit_anchor_seconds=visit_anchor_seconds,
            itinerary_context=itinerary_context,
            before_start_seconds=(
               DateValues.time_value_in_seconds( start_time )
               if start_time is not None
               else None ) ) )

      travel_seconds = WalkTravelTimeCalculator.seconds_between_nodes(
         walk_graph,
         previous_node_id,
         candidate_walk_node_id )

      return max(
         visit_anchor_seconds,
         previous_end_seconds + travel_seconds )


   @classmethod
   def entrance_travel_seconds_to_earliest_item( cls, itinerary: Itinerary ) -> int:
      walk_node_id = cls.walk_node_id_for_earliest_scheduled_item( itinerary )

      if walk_node_id is None:
         return 0

      walk_graph = load_walk_graph()

      return WalkTravelTimeCalculator.seconds_between_nodes(
         walk_graph,
         str( walk_graph[ 'entrance_node_id' ] ),
         walk_node_id )


   @classmethod
   def entrance_travel_seconds_from_latest_item( cls, itinerary: Itinerary ) -> int:
      walk_node_id = cls.walk_node_id_for_latest_scheduled_item( itinerary )

      if walk_node_id is None:
         return 0

      walk_graph = load_walk_graph()

      return WalkTravelTimeCalculator.seconds_between_nodes(
         walk_graph,
         walk_node_id,
         str( walk_graph[ 'entrance_node_id' ] ) )


   @classmethod
   def walk_node_id_for_animal(
         cls,
         *,
         species: str,
         exhibit: str,
         enclosure_name: str | None ) -> str | None:
      return ViewingSpotWalkNodeIdResolver.resolve(
         species,
         exhibit,
         enclosure_name )


   @classmethod
   def walk_node_id_for_attraction( cls, attraction_name: str ) -> str | None:
      walk_node = walk_node_for_map_location(
         MapLocationKind.ATTRACTION,
         attraction_name )

      if walk_node is None:
         return None

      return walk_node.walk_node_id


   @classmethod
   def walk_node_id_for_earliest_scheduled_item(
         cls,
         itinerary: Itinerary ) -> str | None:
      earliest_start_seconds = TimeBlockBuilder.earliest_start_seconds( itinerary )

      if earliest_start_seconds is None:
         return None

      for stop in cls._scheduled_stops_with_walk_nodes( itinerary ):
         if stop.start_seconds == earliest_start_seconds:
            return stop.walk_node_id

      return None


   @classmethod
   def walk_node_id_for_latest_scheduled_item(
         cls,
         itinerary: Itinerary ) -> str | None:
      latest_end_seconds = TimeBlockBuilder.latest_end_seconds( itinerary )

      if latest_end_seconds is None:
         return None

      for transportation in itinerary.transportations:
         end_seconds = DateValues.time_value_in_seconds( transportation.end_time )

         if end_seconds != latest_end_seconds:
            continue

         walk_node_id = TransportationWalkNodeResolver.resolve(
            transportation.name,
            legs=transportation.legs,
            endpoint=TransitRideEndpoint.OFFBOARDING )

         if walk_node_id is not None:
            return walk_node_id

      for stop in cls._scheduled_stops_with_walk_nodes( itinerary ):
         if stop.end_seconds == latest_end_seconds:
            return stop.walk_node_id

      return None


   @classmethod
   def _scheduled_stops_with_walk_nodes(
         cls,
         itinerary: Itinerary ) -> list[ ScheduledWalkStop ]:
      stops: list[ ScheduledWalkStop ] = []

      for animal in itinerary.animals:
         if animal.covered_by_talk:
            continue

         cls._append_scheduled_stop_with_walk_node(
            stops,
            start_time=animal.start_time,
            end_time=animal.end_time,
            walk_node_id=cls.walk_node_id_for_animal(
               species=animal.species,
               exhibit=animal.exhibit,
               enclosure_name=animal.enclosure_name ) )

      for attraction in itinerary.attractions:
         cls._append_scheduled_stop_with_walk_node(
            stops,
            start_time=attraction.start_time,
            end_time=attraction.end_time,
            walk_node_id=cls.walk_node_id_for_attraction( attraction.name ) )

      for transportation in itinerary.transportations:
         cls._append_scheduled_stop_with_walk_node(
            stops,
            start_time=transportation.start_time,
            end_time=transportation.end_time,
            walk_node_id=TransportationWalkNodeResolver.resolve(
               transportation.name,
               legs=transportation.legs ) )

      for talk in itinerary.guardians_talks:
         if talk.is_deleted:
            continue

         walk_node = walk_node_for_map_location(
            MapLocationKind.GUARDIANS_TALK,
            talk.name )

         cls._append_scheduled_stop_with_walk_node(
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

         cls._append_scheduled_stop_with_walk_node(
            stops,
            start_time=encounter.start_time,
            end_time=encounter.end_time,
            walk_node_id=(
               None if walk_node is None else walk_node.walk_node_id ) )

      return stops


   @classmethod
   def _append_scheduled_stop_with_walk_node(
         cls,
         stops: list[ ScheduledWalkStop ],
         *,
         start_time: ScheduleTimeKey,
         end_time: ScheduleTimeKey,
         walk_node_id: str | None ) -> None:
      start_seconds = DateValues.time_value_in_seconds( start_time )
      end_seconds = DateValues.time_value_in_seconds( end_time )

      if start_seconds is None or end_seconds is None or walk_node_id is None:
         return

      stops.append(
         ScheduledWalkStop(
            start_seconds=start_seconds,
            end_seconds=end_seconds,
            walk_node_id=walk_node_id ) )


   @classmethod
   def _previous_stop_end_and_walk_node(
         cls,
         saved_itinerary: SavedItinerary,
         *,
         visit_anchor_seconds: int,
         itinerary_context: dict,
         before_start_seconds: int | None ) -> tuple[ int, str ]:
      walk_graph = load_walk_graph()
      entrance_node_id = str( walk_graph[ 'entrance_node_id' ] )
      itinerary = ItineraryBuilder.build_current( saved_itinerary, **itinerary_context )
      previous_candidates: list[ tuple[ int, str ] ] = [
         ( visit_anchor_seconds, entrance_node_id ),
      ]

      for stop in cls._scheduled_stops_with_walk_nodes( itinerary ):
         if (
               before_start_seconds is not None
               and stop.end_seconds > before_start_seconds ):
            continue

         previous_candidates.append( ( stop.end_seconds, stop.walk_node_id ) )

      return max( previous_candidates, key=lambda item: item[ 0 ] )
