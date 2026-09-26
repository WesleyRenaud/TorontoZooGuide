from __future__ import annotations

from api.shared.calendar_dates import DateValues
from api.shared.enums.position import Position
from api.shared.schedule_row_input import ScheduleRowInput
from api.shared.value_conversion import ValueConversion


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

   assert row is not None
   assert row.time == DateValues.normalize_schedule_time( WIRE_ROW[ 'time' ] )
   assert row.monday is ValueConversion.as_boolean( WIRE_ROW[ 'monday' ] )
   assert row.tuesday is ValueConversion.as_boolean( WIRE_ROW[ 'tuesday' ] )
   assert row.wednesday is ValueConversion.as_boolean( WIRE_ROW[ 'wednesday' ] )
   assert row.thursday is ValueConversion.as_boolean( WIRE_ROW[ 'thursday' ] )
   assert row.friday is ValueConversion.as_boolean( WIRE_ROW[ 'friday' ] )
   assert row.saturday is ValueConversion.as_boolean( WIRE_ROW[ 'saturday' ] )
   assert row.sunday is ValueConversion.as_boolean( WIRE_ROW[ 'sunday' ] )


def Test_ParseRows_TestInvalidAndDuplicateRows_ExpectKeepsFirstValidTimeOnly() -> None:
   first_time = '2:00 PM'
   duplicate_time = '14:00'
   rows = ScheduleRowInput.parse_rows( [
      {
         'time': first_time,
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
         'time': duplicate_time,
         'monday': False,
         'tuesday': True,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
   ] )

   assert [ row.time for row in rows ] == [
      DateValues.normalize_schedule_time( first_time )
   ]
   assert rows[ Position.FIRST ].tuesday is False


def Test_ParseRows_TestEquivalentTimeFormats_ExpectDistinctCanonicalTimesOnly() -> None:
   first_time = '3:30 PM'
   equivalent_time = '15:30'
   later_distinct_time = '14:00'
   rows = ScheduleRowInput.parse_rows( [
      {
         'time': first_time,
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
      {
         'time': equivalent_time,
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
      {
         'time': later_distinct_time,
         'monday': True,
         'tuesday': False,
         'wednesday': False,
         'thursday': False,
         'friday': False,
         'saturday': False,
         'sunday': False,
      },
   ] )

   assert [ row.time for row in rows ] == [
      DateValues.normalize_schedule_time( first_time ),
      DateValues.normalize_schedule_time( later_distinct_time ),
   ]
