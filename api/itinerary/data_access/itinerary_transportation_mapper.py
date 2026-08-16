from __future__ import annotations

from .itinerary_transportation_leg_record import ItineraryTransportationLegRecord
from .itinerary_transportation_record import ItineraryTransportationRecord
from ...types import Row


def map_itinerary_transportation_leg_record(
      row: Row ) -> ItineraryTransportationLegRecord:
   return ItineraryTransportationLegRecord(
      transportation=row[ 'TRANSPORTATION' ],
      from_station=row[ 'FROM_STATION' ],
      to_station=row[ 'TO_STATION' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ] )


def map_itinerary_transportation_record(
      row: Row,
      *,
      legs: list[ ItineraryTransportationLegRecord ] | None = None,
) -> ItineraryTransportationRecord:
   return ItineraryTransportationRecord(
      transportation=row[ 'TRANSPORTATION' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      legs=list( legs or [] ) )


def map_itinerary_transportation_records(
      rows: list[ Row ],
      *,
      legs: list[ ItineraryTransportationLegRecord ] | None = None,
) -> list[ ItineraryTransportationRecord ]:
   legs_by_transportation: dict[ str, list[ ItineraryTransportationLegRecord ] ] = {}

   for leg in legs or []:
      legs_by_transportation.setdefault( leg.transportation, [] ).append( leg )

   return [
      map_itinerary_transportation_record(
         row,
         legs=legs_by_transportation.get( row[ 'TRANSPORTATION' ], [] ) )
      for row in rows
   ]
