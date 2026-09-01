from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import ANIMAL_KEY, expected_departure_time_for_itinerary, LION_ITINERARY_ENTRY, schedule_itinerary_item
from itinerary.support import entrance_travel_seconds_to_animal
from itinerary.support import schedule_time_after_seconds

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from conftest import DbControllers

LION_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Lion',
   exhibit='Africa Savanna' )


def _lion_start_after( anchor_time: str ) -> str:
   return schedule_time_after_seconds( anchor_time, LION_TRAVEL_SECONDS )


def test_date_change_reschedules_animal_before_new_admission_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   scheduled = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY )

   assert scheduled.success
   assert scheduled.itinerary.animals[ 0 ].start_time == _lion_start_after( '9:00 AM' )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   animal_start_seconds = DateValues.time_value_in_seconds(
      result.itinerary.animals[ 0 ].start_time )
   open_seconds = DateValues.time_value_in_seconds( '9:30 AM' )
   assert animal_start_seconds is not None
   assert open_seconds is not None
   assert animal_start_seconds >= open_seconds
   assert result.itinerary.animals[ 0 ].end_time is not None


def test_date_change_reschedules_animal_after_new_closing_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='19:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   scheduled = schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='18:30' )

   assert scheduled.success
   assert scheduled.itinerary.animals[ 0 ].start_time == '6:30 PM'

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-22',
      arrival_time='09:30',
      departure_time='18:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   )

   assert result.success
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )
   assert result.itinerary.animals[ 0 ].start_time == _lion_start_after( '9:30 AM' )
   assert result.itinerary.animals[ 0 ].end_time is not None
