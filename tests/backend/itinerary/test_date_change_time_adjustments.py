from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from conftest import DbControllers


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
   assert result.itinerary.arrival_time == '9:30 AM'
   assert [ adjustment.to_dict() for adjustment in result.adjustments ] == [
      {
         'type': 'arrivalTimeAdjusted',
         'field': 'arrivalTime',
         'previous_value': '9:15 AM',
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
   assert result.itinerary.departure_time == '6:00 PM'
   assert [ adjustment.to_dict() for adjustment in result.adjustments ] == [
      {
         'type': 'departureTimeAdjusted',
         'field': 'departureTime',
         'previous_value': '6:30 PM',
         'value': '18:00',
         'reason': 'departureOutsideOperatingHours',
      },
   ]


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
