from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_set_itinerary_departure_time_must_be_within_zoo_operating_hours(
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

   assert not ItineraryCoordinator.set_departure_time( '09:00' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '5:00 PM'

   assert ItineraryCoordinator.set_departure_time( '18:00' ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '6:00 PM'

   assert not ItineraryCoordinator.set_departure_time( '18:15' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '6:00 PM'


def test_set_itinerary_departure_time_requires_opening_not_early_admission(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='19:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert not ItineraryCoordinator.set_departure_time( '09:00' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '7:00 PM'

   assert ItineraryCoordinator.set_departure_time(
      '09:30',
      confirming_short_visit=True ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '9:30 AM'


def test_set_itinerary_rejects_departure_time_outside_zoo_operating_hours(
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

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='18:15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:30 AM'
   assert itinerary.departure_time == '5:00 PM'


def test_set_itinerary_departure_time_must_be_after_arrival_time(
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

   assert not ItineraryCoordinator.set_departure_time( '09:30' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '5:00 PM'

   assert not ItineraryCoordinator.set_arrival_time( '17:00' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:30 AM'


def test_set_itinerary_departure_time_rejects_visit_shorter_than_two_hours_without_confirmation(
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

   result = ItineraryCoordinator.set_departure_time( '10:00' )

   assert result.status == ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '5:00 PM'


def test_set_itinerary_departure_time_allows_two_hour_visit_without_confirmation(
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

   assert ItineraryCoordinator.set_departure_time( '11:30' ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '11:30 AM'


def test_set_itinerary_rejects_departure_time_that_does_not_follow_arrival(
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

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='10:00',
      departure_time='10:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert not result.success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '9:30 AM'
   assert itinerary.departure_time == '5:00 PM'
