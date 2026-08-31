from __future__ import annotations

from itinerary.support import CAROUSEL

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from conftest import DbControllers


def _set_base_itinerary( db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success


def test_set_arrival_time_none_clears_arrival_time( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '9:30 AM'

   assert ItineraryCoordinator.set_arrival_time( None ).success

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time is None
   assert itinerary.departure_time == '5:00 PM'
