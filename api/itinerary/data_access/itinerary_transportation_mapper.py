from __future__ import annotations

from .itinerary_transportation_record import ItineraryTransportationRecord
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from ...shared.value_conversion import ValueConversion
from ...types import Row


def map_itinerary_transportation_record(
      row: Row,
      *,
      legs: list[ ItineraryTransportationLeg ] | None = None,
) -> ItineraryTransportationRecord:
   return ItineraryTransportationRecord(
      transportation=row[ 'TRANSPORTATION' ],
      old_likelihood=row[ 'OLD_LIKELIHOOD' ],
      new_likelihood=row[ 'NEW_LIKELIHOOD' ],
      start_time=row[ 'START_TIME' ],
      end_time=row[ 'END_TIME' ],
      added_as_attraction=ValueConversion.as_boolean(
         row[ 'ADDED_AS_ATTRACTION' ] ),
      legs=list( legs or [] ) )


def map_itinerary_transportation_records(
      rows: list[ Row ],
      *,
      legs: list[ ItineraryTransportationLeg ] | None = None,
) -> list[ ItineraryTransportationRecord ]:
   legs_by_transportation: dict[ str, list[ ItineraryTransportationLeg ] ] = {}

   for leg in legs or []:
      legs_by_transportation.setdefault( leg.transportation, [] ).append( leg )

   return [
      map_itinerary_transportation_record(
         row,
         legs=legs_by_transportation.get( row[ 'TRANSPORTATION' ], [] ) )
      for row in rows
   ]
