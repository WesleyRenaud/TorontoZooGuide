from __future__ import annotations

from itinerary.support import schedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from conftest import DbControllers


ZOOMOBILE = 'Zoomobile'


def _schedule_zoomobile_as_attraction( db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      transportations=[
         ItineraryTransportationInput(
            name=ZOOMOBILE,
            added_as_attraction=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      'attractions',
      ZOOMOBILE,
      start_time='10:00 AM',
   ).success


def test_fetch_legs_maps_to_itinerary_transportation_leg(
      db: DbControllers,
) -> None:
   _schedule_zoomobile_as_attraction( db )

   legs = ItineraryProvider.fetch_itinerary_transportation_leg_rows( db.conn )

   assert len( legs ) == 5
   assert all( isinstance( leg, ItineraryTransportationLeg ) for leg in legs )
   assert legs[ 0 ].transportation == ZOOMOBILE
   assert legs[ 0 ].from_station == 'Main Zoomobile Station'
   assert legs[ -1 ].to_station == 'Main Zoomobile Station'
