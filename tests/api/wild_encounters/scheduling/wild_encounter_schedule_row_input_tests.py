from __future__ import annotations

from api.wild_encounters.scheduling.wild_encounter_schedule_row_input import WildEncounterScheduleRowInput


WIRE_ROW = {
   'time': '14:00',
   'monday': True,
   'tuesday': False,
   'wednesday': True,
   'thursday': False,
   'friday': True,
   'saturday': False,
   'sunday': True,
}


def Test_FromWire_TestValidRow_ExpectMapsEncounterTimeField() -> None:
   row = WildEncounterScheduleRowInput.from_wire( WIRE_ROW )

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
