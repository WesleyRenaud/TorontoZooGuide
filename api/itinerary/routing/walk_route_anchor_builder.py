from __future__ import annotations

from ..domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from .itinerary_stop import ItineraryStop
from .itinerary_stop_resolver import ItineraryStopResolver
from .itinerary_stop_walk_route_sorter import ItineraryStopWalkRouteSorter
from ...models import Itinerary
from ...models.itinerary_transportation import ItineraryTransportation
from ...shared.calendar_dates import DateValues
from ...shared.enums import ScheduleItemKind
from .transit_ride_endpoint import TransitRideEndpoint
from .transportation_station_walk_node_resolver import TransportationStationWalkNodeResolver
from .transportation_walk_node_resolver import TransportationWalkNodeResolver
from .walk_route_anchor import WalkRouteAnchor


class WalkRouteAnchorBuilder():
   @classmethod
   def build( cls, itinerary: Itinerary ) -> list[ WalkRouteAnchor ]:
      """Ordered walk anchors: content stops plus transportation stations.

      Transit rides replace walking between their board and alight stations.
      Attraction-mode transportation stays a single boarding pin.
      """
      resolved_stops = ItineraryStopResolver.resolve( itinerary )
      content_stops = ItineraryStopWalkRouteSorter.sort(
         [
            stop
            for stop in resolved_stops
            if stop.schedule_item_kind != ScheduleItemKind.TRANSPORTATION
         ] )
      station_anchors = cls._transportation_station_anchors( itinerary )

      if not content_stops and not station_anchors:
         return []

      scheduled_anchors = [
         cls._anchor_from_itinerary_stop( stop )
         for stop in content_stops
         if stop.schedule_item_kind != ScheduleItemKind.ENTRANCE
      ]
      scheduled_anchors.extend( station_anchors )
      scheduled_anchors.sort( key=cls._walk_route_anchor_sort_key )

      if not scheduled_anchors:
         return []

      entrance_stop = next(
         (
            stop
            for stop in content_stops
            if stop.schedule_item_kind == ScheduleItemKind.ENTRANCE
         ),
         None )

      if entrance_stop is None:
         entrance_stop = ItineraryStopResolver.entrance()

      return [
         cls._anchor_from_itinerary_stop( entrance_stop ),
         *scheduled_anchors,
      ]


   @classmethod
   def _transportation_station_anchors(
         cls,
         itinerary: Itinerary,
         ) -> list[ WalkRouteAnchor ]:
      anchors: list[ WalkRouteAnchor ] = []

      for transportation in itinerary.transportations:
         if transportation.added_as_attraction:
            attraction_anchor = cls._attraction_mode_transportation_anchor(
               transportation )

            if attraction_anchor is not None:
               anchors.append( attraction_anchor )

            continue

         anchors.extend(
            cls._transit_ride_station_anchors( transportation ) )

      return anchors


   @classmethod
   def _attraction_mode_transportation_anchor(
         cls,
         transportation: ItineraryTransportation,
         ) -> WalkRouteAnchor | None:
      if not DateValues.normalize_schedule_time_key( transportation.start_time ):
         return None

      if not DateValues.normalize_schedule_time_key( transportation.end_time ):
         return None

      walk_node_id = TransportationWalkNodeResolver.resolve(
         transportation.name,
         legs=transportation.legs )

      if walk_node_id is None:
         return None

      return WalkRouteAnchor(
         schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
         item_key=transportation.name,
         walk_node_ids=[ walk_node_id ],
         start_time=transportation.start_time,
         end_time=transportation.end_time )


   @classmethod
   def _transit_ride_station_anchors(
         cls,
         transportation: ItineraryTransportation,
         ) -> list[ WalkRouteAnchor ]:
      anchors: list[ WalkRouteAnchor ] = []
      sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences(
         transportation.legs )

      for sequence_index, sequence in enumerate( sequences ):
         onboarding_station = sequence[ 0 ].from_station
         offboarding_station = sequence[ -1 ].to_station
         onboarding_node_id = TransportationStationWalkNodeResolver.resolve(
            transportation.name,
            onboarding_station )
         offboarding_node_id = TransportationStationWalkNodeResolver.resolve(
            transportation.name,
            offboarding_station )
         ride_key = f'{ transportation.name }||{ sequence_index }'
         onboarding_time = sequence[ 0 ].start_time
         offboarding_time = sequence[ -1 ].end_time

         if onboarding_node_id is not None:
            anchors.append(
               WalkRouteAnchor(
                  schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
                  item_key=f'{ ride_key }||{ onboarding_station }',
                  walk_node_ids=[ onboarding_node_id ],
                  start_time=onboarding_time,
                  end_time=onboarding_time,
                  transit_ride_key=ride_key,
                  transit_endpoint=TransitRideEndpoint.ONBOARDING ) )

         if offboarding_node_id is not None:
            anchors.append(
               WalkRouteAnchor(
                  schedule_item_kind=ScheduleItemKind.TRANSPORTATION,
                  item_key=f'{ ride_key }||{ offboarding_station }',
                  walk_node_ids=[ offboarding_node_id ],
                  start_time=offboarding_time,
                  end_time=offboarding_time,
                  transit_ride_key=ride_key,
                  transit_endpoint=TransitRideEndpoint.OFFBOARDING ) )

      return anchors


   @classmethod
   def _anchor_from_itinerary_stop( cls, stop: ItineraryStop ) -> WalkRouteAnchor:
      return WalkRouteAnchor(
         schedule_item_kind=stop.schedule_item_kind,
         item_key=stop.item_key,
         walk_node_ids=list( stop.walk_node_ids ),
         start_time=stop.start_time,
         end_time=stop.end_time )


   @classmethod
   def _walk_route_anchor_sort_key(
         cls,
         anchor: WalkRouteAnchor,
         ) -> tuple[ int, int, str, str ]:
      start_seconds = DateValues.time_value_in_seconds( anchor.start_time )

      return (
         start_seconds if start_seconds is not None else 0,
         (
            int( anchor.transit_endpoint )
            if anchor.transit_endpoint is not None
            else len( TransitRideEndpoint )
         ),
         anchor.schedule_item_kind.value,
         anchor.item_key.lower(),
      )
