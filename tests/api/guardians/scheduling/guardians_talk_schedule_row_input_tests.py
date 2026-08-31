from __future__ import annotations

from api.guardians.scheduling.guardians_talk_schedule_row_input import GuardiansTalkScheduleRowInput


WIRE_ROW = {
   'time': '10:00',
   'monday': True,
   'tuesday': False,
   'wednesday': True,
   'thursday': False,
   'friday': False,
   'saturday': False,
   'sunday': False,
}


def Test_FromWire_TestValidRow_ExpectMapsTalkTimeField() -> None:
   row = GuardiansTalkScheduleRowInput.from_wire( WIRE_ROW )

   assert row == GuardiansTalkScheduleRowInput(
      talk_time='10:00 AM',
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
   )


def Test_ParseRows_TestMultipleTimes_ExpectDistinctTalkTimes() -> None:
   rows = GuardiansTalkScheduleRowInput.parse_rows( [
      {
         'time': '14:00',
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
      {
         'time': '15:30',
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
   ] )

   assert [ row.talk_time for row in rows ] == [ '2:00 PM', '3:30 PM' ]
