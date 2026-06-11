from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from conftest import DbControllers

def test_set_itinerary_arrival_and_departure_time_updates_only_requested_field(
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

   assert ItineraryCoordinator.set_arrival_time( '10:15 AM' ).success
   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '10:15'
   assert itinerary.departure_time == '17:00'

   assert ItineraryCoordinator.set_arrival_time( None ).success
   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time is None
   assert itinerary.departure_time == '17:00'

   assert ItineraryCoordinator.set_arrival_time( '10:15 AM' ).success
   assert ItineraryCoordinator.set_departure_time( None ).success
   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '10:15'
   assert itinerary.departure_time is None


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
   assert itinerary.arrival_time == '09:30'

   assert ItineraryCoordinator.set_departure_time( '18:00' ).success
   assert ItineraryCoordinator.set_arrival_time(
      '17:00',
      confirming_short_visit=True ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '17:00'
   assert itinerary.departure_time == '18:00'

   assert not ItineraryCoordinator.set_arrival_time( '17:15' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '17:00'


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
   assert itinerary.arrival_time == '09:00'

   assert not ItineraryCoordinator.set_arrival_time( '08:45' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '09:00'


def test_set_itinerary_date_change_adjusts_arrival_when_early_admission_is_unavailable(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:15',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary.arrival_time == '09:30'
   assert [ adjustment.to_dict() for adjustment in result.adjustments ] == [
      {
         'type': 'arrivalTimeAdjusted',
         'field': 'arrivalTime',
         'previous_value': '09:15',
         'value': '09:30',
         'reason': 'arrivalOutsideAdmissionHours',
      },
   ]


def test_set_itinerary_date_change_adjusts_departure_when_close_time_is_earlier(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='18:30',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary.departure_time == '18:00'
   assert [ adjustment.to_dict() for adjustment in result.adjustments ] == [
      {
         'type': 'departureTimeAdjusted',
         'field': 'departureTime',
         'previous_value': '18:30',
         'value': '18:00',
         'reason': 'departureOutsideOperatingHours',
      },
   ]


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
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


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
   assert itinerary.departure_time == '17:00'

   assert ItineraryCoordinator.set_departure_time( '18:00' ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '18:00'

   assert not ItineraryCoordinator.set_departure_time( '18:15' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '18:00'


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
   assert itinerary.departure_time == '19:00'

   assert ItineraryCoordinator.set_departure_time(
      '09:30',
      confirming_short_visit=True ).success
   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.departure_time == '09:30'


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
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


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
   assert itinerary.departure_time == '17:00'

   assert not ItineraryCoordinator.set_arrival_time( '17:00' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '09:30'


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
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


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
   assert itinerary.arrival_time == '16:30'
   assert itinerary.departure_time == '17:00'


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
   assert itinerary.departure_time == '17:00'


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
   assert itinerary.departure_time == '11:30'


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
   assert itinerary.arrival_time == '09:30'
   assert itinerary.departure_time == '17:00'


def test_set_itinerary_normalizes_display_format_schedule_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Grizzly Bear',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='1:00 PM',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ 'Grizzly Bear' ],
   ).success

   encounter_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'Grizzly Bear';
      """ ).fetchone()

   assert dict( encounter_schedule ) == {
      'START_TIME': '13:00',
      'END_TIME': '13:45',
   }

def test_get_zoo_hours_returns_seeded_operating_bounds( db: DbControllers ) -> None:
   assert ZooHoursCoordinator.get_zoo_hours( day=20, month='June', year=2026 ).to_dict() == {
      'date': '2026-06-20',
      'earlyAdmissionTime': '09:00',
      'openTime': '09:30',
      'lastAdmissionTime': '18:00',
      'closeTime': '19:00'
   }

   assert ZooHoursCoordinator.get_zoo_hours( day=22, month='June', year=2026 ).to_dict() == {
      'date': '2026-06-22',
      'earlyAdmissionTime': None,
      'openTime': '09:30',
      'lastAdmissionTime': '17:00',
      'closeTime': '18:00'
   }

   assert ZooHoursCoordinator.get_zoo_hours( day=25, month='December', year=2026 ).to_dict() == {
      'date': '2026-12-25',
      'earlyAdmissionTime': None,
      'openTime': '11:00',
      'lastAdmissionTime': '15:00',
      'closeTime': '16:00'
   }

