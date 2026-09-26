from __future__ import annotations

from collections.abc import Callable
from datetime import date
from datetime import datetime
from datetime import time

from api_test_support.frozen_datetime import patch_database_today
import pytest

from api.shared.calendar_dates import DateValues
from api.types import Types


MISSING_START_FALLBACK_DATE = date( 2026, 6, 15 )


@pytest.fixture
def freeze_database_today( monkeypatch: pytest.MonkeyPatch ) -> Callable[ [ date ], None ]:
   def freeze( value: date ) -> None:
      patch_database_today( monkeypatch, value )

   return freeze


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( date( 2026, 6, 15 ), date( 2026, 6, 15 ) ),
      ( datetime( 2026, 6, 15, 9, 30 ), date( 2026, 6, 15 ) ),
      ( '2026-06-15', date( 2026, 6, 15 ) ),
      ( '2026-06-15 09:30', date( 2026, 6, 15 ) )
   ]
)
def Test_ParseDateValue( value: Types.DateInput, expected: date | None ) -> None:
   parsed = DateValues.parse_date_value( value )

   assert parsed == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '  ', None ),
      ( '2026-06-15', '2026-06-15' ),
      ( date( 2026, 6, 15 ), '2026-06-15' ),
      ( datetime( 2026, 6, 15, 9, 30 ), '2026-06-15' ),
   ]
)
def Test_normalize_date_key( value: Types.DateInput, expected: Types.DateKey | None ) -> None:
   date_key = DateValues.normalize_date_key( value )

   assert date_key == expected


def Test_NormalizeDateKey_TestUnsupportedDateStrings_ExpectNone() -> None:
   value = 'June 15, 2026'

   date_key = DateValues.normalize_date_key( value )

   assert date_key is None


def Test_ResolveOpenEndedDateRange_TestOpenEndDate_ExpectPreserved() -> None:
   start_date = '2026-06-01'
   end_date = None

   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   assert date_range.start_date == start_date
   assert date_range.end_date is None


def Test_ResolveOpenEndedDateRange_TestMissingStart_ExpectUsesFrozenToday(
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( MISSING_START_FALLBACK_DATE )

   date_range = DateValues.resolve_open_ended_date_range(
      start_date=None,
      end_date=None )

   assert date_range.start_date == MISSING_START_FALLBACK_DATE.isoformat()
   assert date_range.end_date is None


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '2026-06-15 09:30 AM', datetime( 2026, 6, 15, 9, 30 ) ),
      ( '2026-06-15 17:45:00', datetime( 2026, 6, 15, 17, 45 ) ),
      ( '2026-06-15 17:45', datetime( 2026, 6, 15, 17, 45 ) )
   ]
)
def Test_parse_datetime_value( value: str | None, expected: datetime | None ) -> None:
   parsed = DateValues.parse_datetime_value( value )

   assert parsed == expected


def Test_ParseDateValue_TestUnsupportedFormat_ExpectValueError() -> None:
   value = 'June 15, 2026'

   with pytest.raises( ValueError ):
      DateValues.parse_date_value( value )


def Test_ParseDatetimeValue_TestUnsupportedFormat_ExpectValueError() -> None:
   value = 'June 15, 2026 9:30'

   with pytest.raises( ValueError ):
      DateValues.parse_datetime_value( value )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '   ', None ),
      ( '1:00 PM', '1:00 PM' ),
      ( '13:45', '1:45 PM' ),
      ( '13:45:30', '1:45:30 PM' ),
      ( '10:00', '10:00 AM' ),
      ( 'not-a-time', None ),
   ]
)
def Test_normalize_schedule_time(
      value: str | None,
      expected: str | None ) -> None:
   normalized = DateValues.normalize_schedule_time( value )

   assert normalized == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( '   ', None ),
      ( '1:00 PM', '1:00 PM' ),
      ( '13:45', '1:45 PM' ),
      ( '13:45:30', '1:45:30 PM' ),
      ( '10:00', '10:00 AM' ),
      ( 'not-a-time', None ),
   ]
)
def Test_normalize_itinerary_schedule_time(
      value: str | None,
      expected: str | None ) -> None:
   normalized = DateValues.normalize_itinerary_schedule_time( value )

   assert normalized == expected


@pytest.mark.parametrize(
   'values, expected',
   [
      ( [], [] ),
      ( [ '2:00 PM', '3:30 PM' ], [ '2:00 PM', '3:30 PM' ] ),
      ( [ '3:30 PM', '15:30', '2:00 PM' ], [ '3:30 PM', '2:00 PM' ] ),
      ( [ '1:00 PM', 'not-a-time', '13:00' ], [ '1:00 PM' ] ),
   ]
)
def Test_normalize_unique_schedule_times(
      values: list[ str ],
      expected: list[ str ] ) -> None:
   unique_times = DateValues.normalize_unique_schedule_times( values )

   assert unique_times == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, '' ),
      ( '', '' ),
      ( '   ', '' ),
      ( '09:30', '09:30' ),
      ( ' 1:00 PM ', '1:00 PM' ),
   ]
)
def Test_normalize_schedule_time_key(
      value: str | None,
      expected: str ) -> None:
   time_key = DateValues.normalize_schedule_time_key( value )

   assert time_key == expected


def Test_TimeValueInSeconds_TestNone_ExpectNone() -> None:
   value = None

   seconds = DateValues.time_value_in_seconds( value )

   assert seconds is None


def Test_TimeValueInSeconds_TestHoursAndMinutes_ExpectSeconds() -> None:
   hours = 9
   minutes = 30
   value = time( hours, minutes ).strftime( '%H:%M' )

   seconds = DateValues.time_value_in_seconds( value )

   assert seconds == hours * 3600 + minutes * 60


def Test_TimeValueInSeconds_TestHoursMinutesSeconds_ExpectSeconds() -> None:
   hours = 9
   minutes = 30
   extra_seconds = 30
   value = time( hours, minutes, extra_seconds ).strftime( '%H:%M:%S' )

   seconds = DateValues.time_value_in_seconds( value )

   assert seconds == hours * 3600 + minutes * 60 + extra_seconds


def Test_TimeValueInSeconds_TestAfternoonClock_ExpectSeconds() -> None:
   value = '1:00 PM'

   seconds = DateValues.time_value_in_seconds( value )

   assert seconds == DateValues.time_value_in_seconds(
      DateValues.parse_time_value( value ) )


def Test_TimeValueIsAtOrAfter_TestEqualTimes_ExpectTrue() -> None:
   same_time = '10:30 AM'

   is_at_or_after = DateValues.time_value_is_at_or_after( same_time, same_time )

   assert is_at_or_after


def Test_TimeValueIsAtOrAfter_TestLaterTime_ExpectTrue() -> None:
   later = '10:30 AM'
   earlier = '10:15 AM'

   is_at_or_after = DateValues.time_value_is_at_or_after( later, earlier )

   assert is_at_or_after is (
      DateValues.time_value_in_seconds( later )
      >= DateValues.time_value_in_seconds( earlier ) )


def Test_TimeValueIsAtOrAfter_TestEarlierTime_ExpectFalse() -> None:
   earlier = '10:15 AM'
   later = '10:30 AM'

   is_at_or_after = DateValues.time_value_is_at_or_after( earlier, later )

   assert is_at_or_after is (
      DateValues.time_value_in_seconds( earlier )
      >= DateValues.time_value_in_seconds( later ) )


def Test_TimeValueIsAtOrAfter_TestMissingLeft_ExpectFalse() -> None:
   left = None
   right = '10:30 AM'

   is_at_or_after = DateValues.time_value_is_at_or_after( left, right )

   assert is_at_or_after is False


def Test_TimeValueIsAtOrAfter_TestMissingRight_ExpectFalse() -> None:
   left = '10:30 AM'
   right = None

   is_at_or_after = DateValues.time_value_is_at_or_after( left, right )

   assert is_at_or_after is False


def Test_ScheduleTimeKeyFromSeconds_TestHoursAndMinutes_ExpectDisplayTime() -> None:
   hours = 9
   minutes = 30
   total_seconds = hours * 3600 + minutes * 60

   key = DateValues.schedule_time_key_from_seconds( total_seconds )

   assert key == DateValues.format_display_time_value( time( hours, minutes ) )


def Test_ScheduleTimeKeyFromSeconds_TestWithSeconds_ExpectDisplayTime() -> None:
   hours = 9
   minutes = 30
   extra_seconds = 30
   total_seconds = hours * 3600 + minutes * 60 + extra_seconds

   key = DateValues.schedule_time_key_from_seconds( total_seconds )

   assert key == DateValues.format_display_time_value(
      time( hours, minutes, extra_seconds ) )


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', False ),
      ( date( 2026, 6, 16 ), '2026-06-14', True ),
   ]
)
def Test_is_date_on_or_after( left: date, right: Types.DateInput, expected: bool ) -> None:
   is_on_or_after = DateValues.is_date_on_or_after( left, right )

   assert is_on_or_after is expected


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 16 ), '2026-06-15', False ),
      ( date( 2026, 6, 14 ), '2026-06-14', True ),
   ]
)
def Test_is_date_on_or_before( left: date, right: Types.DateInput, expected: bool ) -> None:
   is_on_or_before = DateValues.is_date_on_or_before( left, right )

   assert is_on_or_before is expected


@pytest.mark.parametrize(
   'target, start, end, expected',
   [
      ( date( 2026, 6, 15 ), None, None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', None, False ),
      ( date( 2026, 6, 16 ), None, '2026-06-15', False )
   ]
)
def Test_is_date_in_range(
      target: date,
      start: Types.DateInput,
      end: Types.DateInput,
      expected: bool ) -> None:
   in_range = DateValues.is_date_in_range(
      target_date=target,
      start_date_value=start,
      end_date_value=end )

   assert in_range is expected


def Test_ParseTimeValue_TestDatetimeInput_ExpectTimeComponent() -> None:
   value = datetime( 2026, 6, 15, 14, 30, 45 )

   parsed = DateValues.parse_time_value( value )

   assert parsed == value.time()


def Test_FormatTimeValue_TestSecondsPresent_ExpectHmsFormat() -> None:
   value = '14:30:45'

   formatted = DateValues.format_time_value( value )

   assert formatted == value


def Test_ScheduleTimeKeyFromSeconds_TestInvalidSeconds_ExpectValueError() -> None:
   total_seconds = -1

   with pytest.raises( ValueError ):
      DateValues.schedule_time_key_from_seconds( total_seconds )


def Test_ScheduleTimeKeyFromMinutes_TestInvalidMinutes_ExpectValueError() -> None:
   minutes = -5

   with pytest.raises( ValueError ):
      DateValues.schedule_time_key_from_minutes( minutes )


def Test_AddMinutesToTime_TestZeroDuration_ExpectNone() -> None:
   start_time = '10:00 AM'
   minutes = 0

   result = DateValues.add_minutes_to_time( start_time, minutes )

   assert result is None


def Test_AddMinutesToTime_TestNegativeDuration_ExpectNone() -> None:
   start_time = '10:00 AM'
   minutes = -5

   result = DateValues.add_minutes_to_time( start_time, minutes )

   assert result is None


def Test_NormalizeDateKey_TestInvalidDate_ExpectNone() -> None:
   value = 'not-a-date'

   date_key = DateValues.normalize_date_key( value )

   assert date_key is None


def Test_FormatDisplayDateValue_TestValidDate_ExpectMonthDayYear() -> None:
   value = '2026-06-15'
   parsed = DateValues.parse_date_value( value )

   display = DateValues.format_display_date_value( value )

   assert display == f'{ parsed.strftime( "%B" ) } { parsed.day }, { parsed.year }'


def Test_FormatDisplayDateValue_TestInvalidDate_ExpectNone() -> None:
   value = None

   display = DateValues.format_display_date_value( value )

   assert display is None


def Test_FormatTimeValue_TestEmptyTime_ExpectNone() -> None:
   value = ''

   formatted = DateValues.format_time_value( value )

   assert formatted is None


def Test_FormatTimeValue_TestWithoutSeconds_ExpectHmFormat() -> None:
   value = '14:30'

   formatted = DateValues.format_time_value( value )

   assert formatted == value


def Test_NormalizeUniqueItineraryScheduleTimes_TestDelegates_ExpectUniqueTimes() -> None:
   times = [ '10:00 AM', '10:00 AM', '11:00 AM' ]

   unique_times = DateValues.normalize_unique_itinerary_schedule_times( times )

   assert unique_times == DateValues.normalize_unique_schedule_times( times )


def Test_ScheduleTimeKeyFromSeconds_TestFormatReturnsNone_ExpectValueError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      DateValues,
      'format_display_time_value',
      lambda _time: None )

   with pytest.raises( ValueError, match='Invalid schedule time seconds' ):
      DateValues.schedule_time_key_from_seconds( 3600 )


def Test_ScheduleTimeKeyFromMinutes_TestFormatReturnsNone_ExpectValueError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      DateValues,
      'format_display_time_value',
      lambda _time: None )

   with pytest.raises( ValueError, match='Invalid schedule time minutes' ):
      DateValues.schedule_time_key_from_minutes( 90 )


def Test_NormalizeDateKey_TestParseReturnsNone_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   value = '2026-06-15'
   monkeypatch.setattr(
      DateValues,
      'parse_date_value',
      lambda _value: None )

   date_key = DateValues.normalize_date_key( value )

   assert date_key is None
