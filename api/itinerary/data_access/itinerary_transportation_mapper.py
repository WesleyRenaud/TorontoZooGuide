from __future__ import annotations

from .itinerary_transportation_record import ItineraryTransportationRecord
from .itinerary_transportation_route_marker_mapper import route_marker_sequences_for_markers
from .itinerary_transportation_route_marker_record import ItineraryTransportationRouteMarkerRecord
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.calendar_dates import DateValues
from ...shared.value_conversion import ValueConversion
from ...types import Row


TransportationRowKey = tuple[ str, bool ]


def transportation_row_key(
      transportation: str,
      added_as_attraction: bool ) -> TransportationRowKey:
   return ( transportation, added_as_attraction )


def map_itinerary_transportation_record(
      row: Row,
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
      bulk_transit_evaluated=ValueConversion.as_boolean(
         row[ 'BULK_TRANSIT_EVALUATED' ] ),
      legs=sorted(
         legs,
         key=lambda leg: DateValues.time_value_in_seconds( leg.start_time ) ),
      route_marker_sequences=route_marker_sequences_for_markers( route_markers ),
   )


def map_itinerary_transportation_records(
      rows: list[ Row ],
      legs: list[ ItineraryTransportationLeg ],
      route_markers: list[ ItineraryTransportationRouteMarkerRecord ],
) -> list[ ItineraryTransportationRecord ]:
   legs_by_transportation: dict[
      TransportationRowKey,
      list[ ItineraryTransportationLeg ],
   ] = {}
   markers_by_transportation: dict[
      TransportationRowKey,
      list[ ItineraryTransportationRouteMarkerRecord ],
   ] = {}

   for leg in legs:
      key = transportation_row_key(
         leg.transportation,
         added_as_attraction=leg.added_as_attraction )
      legs_by_transportation.setdefault( key, [] ).append( leg )

   for marker in route_markers:
      key = transportation_row_key(
         marker.transportation,
         added_as_attraction=marker.added_as_attraction )
      markers_by_transportation.setdefault( key, [] ).append( marker )

   return [
      map_itinerary_transportation_record(
         row,
         legs=legs_by_transportation.get(
            transportation_row_key(
               row[ 'TRANSPORTATION' ],
               added_as_attraction=ValueConversion.as_boolean(
                  row[ 'ADDED_AS_ATTRACTION' ] ),
            ),
            [],
         ),
         route_markers=markers_by_transportation.get(
            transportation_row_key(
               row[ 'TRANSPORTATION' ],
               added_as_attraction=ValueConversion.as_boolean(
                  row[ 'ADDED_AS_ATTRACTION' ] ),
            ),
            [],
         ),
      )
      for row in rows
   ]
