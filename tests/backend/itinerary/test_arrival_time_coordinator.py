from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_set_itinerary_arrival_time_must_be_within_zoo_admission_hours(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert not ItineraryCoordinator.set_arrival_time( '09:00' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:30 AM'

   assert ItineraryCoordinator.set_departure_time( '18:00' ).success
   assert ItineraryCoordinator.set_arrival_time(
      '17:00',
      confirming_short_visit=True ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '5:00 PM'
   assert itinerary.departure_time == '6:00 PM'

   assert not ItineraryCoordinator.set_arrival_time( '17:15' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '5:00 PM'


def test_set_itinerary_arrival_time_allows_early_admission_when_offered(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:00 AM'

   assert not ItineraryCoordinator.set_arrival_time( '08:45' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:00 AM'


def test_set_itinerary_rejects_arrival_time_outside_zoo_admission_hours(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='17:15',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:30 AM'
   assert itinerary.departure_time == '5:00 PM'


def test_set_itinerary_arrival_time_rejects_visit_shorter_than_two_hours_without_confirmation(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.set_arrival_time( '16:30' )

   assert result.status == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:30 AM'
   assert itinerary.departure_time == '5:00 PM'


def test_set_itinerary_arrival_time_allows_short_visit_with_confirmation(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.set_arrival_time(
      '16:30',
      confirming_short_visit=True )

   assert result.success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '4:30 PM'
   assert itinerary.departure_time == '5:00 PM'
