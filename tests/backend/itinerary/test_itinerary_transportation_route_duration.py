from __future__ import annotations

from datetime import date

from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.domain.itinerary_transportations_builder import ItineraryTransportationsBuilder
from conftest import DbControllers


def test_build_itinerary_transportations_includes_route_duration(
      db: DbControllers,
) -> None:
   transportations = ItineraryTransportationsBuilder.build(
      [
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=None,
            start_time=None,
            end_time=None,
            legs=[],
            added_as_attraction=False,
         ),
      ],
      target_date=date( 2026, 6, 15 ),
   )

   assert len( transportations ) == 1
   assert transportations[ 0 ].route_duration_minutes == 75
