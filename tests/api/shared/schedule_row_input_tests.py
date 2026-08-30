from __future__ import annotations

from api.shared.schedule_row_input import ScheduleRowInput


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


def Test_FromWire_TestValidRow_ExpectNormalizesTimeAndDayFlags() -> None:
   row = ScheduleRowInput.from_wire( WIRE_ROW )

   assert row == ScheduleRowInput(
      time='2:00 PM',
      monday=True,
      tuesday=False,
      wednesday=True,
      thursday=False,
      friday=True,
      saturday=False,
      sunday=True,
   )


def Test_ParseRows_TestInvalidAndDuplicateRows_ExpectKeepsFirstValidTimeOnly() -> None:
   rows = ScheduleRowInput.parse_rows( [
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

   assert [ row.time for row in rows ] == [ '2:00 PM' ]
   assert rows[ 0 ].tuesday is False
