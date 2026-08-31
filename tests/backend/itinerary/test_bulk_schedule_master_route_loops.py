from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CHEETAH_ITINERARY_ENTRY, LION_ITINERARY_ENTRY, PENGUIN_ITINERARY_ENTRY, wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_row

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def _set_midday_rhino_encounter_schedule() -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Guardians of White Rhinos',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row(
            '09:52',
            monday=False,
            tuesday=False,
            wednesday=False,
            thursday=False,
            friday=False,
            saturday=True,
            sunday=False,
         ),
      ],
      message=None,
   )


def test_bulk_schedule_itinerary_keeps_master_route_loop_on_one_side_of_wild_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_midday_rhino_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( 'Guardians of White Rhinos', start_time='09:52' ),
      ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []

   loop_animals = [
      animal for animal in result.itinerary.animals
      if animal.species in { 'African Lion', 'African Penguin', 'Cheetah' }
      and animal.exhibit == 'Africa Savanna'
   ]

   assert len( loop_animals ) == 3
   assert all(
      animal.start_time is not None and animal.end_time is not None
      for animal in loop_animals )

   encounter_start_seconds = DateValues.time_value_in_seconds( '09:52 AM' )
   encounter_end_seconds = DateValues.time_value_in_seconds( '10:37 AM' )

   assert encounter_start_seconds is not None
   assert encounter_end_seconds is not None

   start_times = [
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in loop_animals
   ]
   end_times = [
      DateValues.time_value_in_seconds( animal.end_time )
      for animal in loop_animals
   ]

   assert all( start_time is not None for start_time in start_times )
   assert all( end_time is not None for end_time in end_times )

   all_before_encounter = all(
      end_time <= encounter_start_seconds
      for end_time in end_times
      if end_time is not None )
   all_after_encounter = all(
      start_time >= encounter_end_seconds
      for start_time in start_times
      if start_time is not None )

   assert all_before_encounter or all_after_encounter

   for start_time, end_time in zip( start_times, end_times ):
      assert start_time is not None
      assert end_time is not None
      assert not (
            start_time < encounter_start_seconds
            and end_time > encounter_start_seconds )
