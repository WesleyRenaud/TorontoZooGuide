from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_row

from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.scheduling.wild_encounter_day_schedule_finder import WildEncounterDayScheduleFinder
from conftest import DbControllers


def test_wild_encounter_day_schedule_uses_active_record_when_expired_row_also_exists(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 9 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-28',
      end_date='2026-07-05',
      schedule_rows=[
         wire_schedule_row(
            '3:30 PM',
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
         ),
      ],
      message=None,
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-07-06',
      end_date=None,
      schedule_rows=[
         wire_schedule_row(
            '3:30 PM',
            monday=True,
            tuesday=True,
            wednesday=True,
            thursday=True,
            friday=True,
            saturday=True,
            sunday=True,
         ),
      ],
      message=None,
   )

   day_schedule = WildEncounterCoordinator.get_wild_encounter_schedule(
      month=7,
      day=9,
      year=2026 )
   kangaroo_slots = [
      item
      for item in day_schedule
      if item.name == 'Kangaroo' and item.start_time == '3:30 PM'
   ]

   assert len( kangaroo_slots ) == 1
   assert kangaroo_slots[ 0 ].is_available

   match = WildEncounterDayScheduleFinder.find_on_day_schedule(
      day_schedule,
      'Kangaroo',
      start_time='3:30 PM' )

   assert match is not None
   assert match.is_available
