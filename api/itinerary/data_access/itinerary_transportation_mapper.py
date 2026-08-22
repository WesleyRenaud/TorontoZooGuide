from __future__ import annotations

from .itinerary_transportation_record import ItineraryTransportationRecord
from .itinerary_transportation_route_marker_mapper import route_marker_sequences_for_markers
from .itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.value_conversion import ValueConversion
from ...types import Row


def map_itinerary_transportation_record(
      row: Row,
      *,
      legs: list[ ItineraryTransportationLeg ],
      route_markers: list[ ItineraryTransportationRouteMarkerRecord ],
) -> ItineraryTransportationRecord:
   return ItineraryTransportationRecord(
      transportation=row[ 'TRANSPORTATION' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      added_as_attraction=ValueConversion.as_boolean(
         row[ 'ADDED_AS_ATTRACTION' ] ),
      route=row[ 'ROUTE' ],
      legs=legs,
      route_marker_sequences=route_marker_sequences_for_markers( route_markers ),
   )


def map_itinerary_transportation_records(
      rows: list[ Row ],
      *,
      legs: list[ ItineraryTransportationLeg ],
      route_markers: list[ ItineraryTransportationRouteMarkerRecord ],
) -> list[ ItineraryTransportationRecord ]:
   legs_by_transportation: dict[ str, list[ ItineraryTransportationLeg ] ] = {}
   markers_by_transportation: dict[
      str,
      list[ ItineraryTransportationRouteMarkerRecord ],
   ] = {}

   for leg in legs:
      legs_by_transportation.setdefault( leg.transportation, [] ).append( leg )

   for marker in route_markers:
      markers_by_transportation.setdefault(
         marker.transportation,
         [],
      ).append( marker )

   return [
      map_itinerary_transportation_record(
         row,
         legs=legs_by_transportation.get( row[ 'TRANSPORTATION' ], [] ),
         route_markers=markers_by_transportation.get(
            row[ 'TRANSPORTATION' ],
            [],
         ),
      )
      for row in rows
   ]
