from __future__ import annotations

from api.wild_encounters.scheduling.wild_encounter_schedule_row_input import WildEncounterScheduleRowInput


def test_wild_encounter_schedule_row_from_wire_normalizes_time_and_day_flags() -> None:
   row = WildEncounterScheduleRowInput.from_wire( {
      'time': '14:00',
      'monday': True,
      'tuesday': False,
      'wednesday': True,
      'thursday': False,
      'friday': True,
      'saturday': False,
      'sunday': True,
   } )

   assert row == WildEncounterScheduleRowInput(
      encounter_time='2:00 PM',
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=True,
      saturday=False,
      sunday=True,
   )


def test_parse_wild_encounter_schedule_rows_skips_invalid_rows_and_duplicate_times() -> None:
   rows = WildEncounterScheduleRowInput.parse_rows( [
      {
         'time': '2:00 PM',
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
      'bad-row',
      {
         'time': '',
         'monday': True,
      },
      {
         'time': '14:00',
         'monday': False,
         'tuesday': True,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
   ] )

   assert [ row.encounter_time for row in rows ] == [ '2:00 PM' ]
   assert rows[ 0 ].tuesday is False
