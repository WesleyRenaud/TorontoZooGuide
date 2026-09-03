from __future__ import annotations

from collections.abc import Callable
from datetime import date
from datetime import datetime

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
   assert DateValues.parse_date_value( value ) == expected


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
   assert DateValues.normalize_date_key( value ) == expected


def Test_NormalizeDateKey_TestUnsupportedDateStrings_ExpectNone() -> None:
   assert DateValues.normalize_date_key( 'June 15, 2026' ) is None


def Test_ResolveOpenEndedDateRange_TestOpenEndDate_ExpectPreserved() -> None:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date='2026-06-01',
      end_date=None )

   assert date_range.start_date == '2026-06-01'
   assert date_range.end_date is None


def Test_ResolveOpenEndedDateRange_TestMissingStart_ExpectUsesFrozenToday(
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( MISSING_START_FALLBACK_DATE )

   date_range = DateValues.resolve_open_ended_date_range(
      start_date=None,
      end_date=None )

   assert date_range.start_date == '2026-06-15'
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
   assert DateValues.parse_datetime_value( value ) == expected


def Test_ParseValues_TestUnsupportedFormats_ExpectValueError() -> None:
   with pytest.raises( ValueError ):
      DateValues.parse_date_value( 'June 15, 2026' )

   with pytest.raises( ValueError ):
      DateValues.parse_datetime_value( 'June 15, 2026 9:30' )


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
   assert DateValues.normalize_schedule_time( value ) == expected


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
   assert DateValues.normalize_itinerary_schedule_time( value ) == expected


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
   assert DateValues.normalize_unique_schedule_times( values ) == expected


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
   assert DateValues.normalize_schedule_time_key( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '09:30', 9 * 3600 + 30 * 60 ),
      ( '09:30:30', 9 * 3600 + 30 * 60 + 30 ),
      ( '1:00 PM', 13 * 3600 ),
   ]
)
def Test_time_value_in_seconds(
      value: str | None,
      expected: int | None ) -> None:
   assert DateValues.time_value_in_seconds( value ) == expected


def Test_TimeValueIsAtOrAfter_TestVariousPairs_ExpectComparisonResult() -> None:
   assert DateValues.time_value_is_at_or_after( '10:30 AM', '10:30 AM' )
   assert DateValues.time_value_is_at_or_after( '10:30 AM', '10:15 AM' )
   assert not DateValues.time_value_is_at_or_after( '10:15 AM', '10:30 AM' )
   assert not DateValues.time_value_is_at_or_after( None, '10:30 AM' )
   assert not DateValues.time_value_is_at_or_after( '10:30 AM', None )


@pytest.mark.parametrize(
   'total_seconds, expected',
   [
      ( 9 * 3600 + 30 * 60, '9:30 AM' ),
      ( 9 * 3600 + 30 * 60 + 30, '9:30:30 AM' ),
   ]
)
def Test_schedule_time_key_from_seconds(
      total_seconds: int,
      expected: str ) -> None:
   assert DateValues.schedule_time_key_from_seconds( total_seconds ) == expected


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
   assert DateValues.is_date_on_or_after( left, right ) is expected


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
   assert DateValues.is_date_on_or_before( left, right ) is expected


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
   assert DateValues.is_date_in_range( target_date=target, start_date_value=start, end_date_value=end ) is expected


def Test_ParseTimeValue_TestDatetimeInput_ExpectTimeComponent() -> None:
   assert DateValues.parse_time_value( datetime( 2026, 6, 15, 14, 30, 45 ) ) == datetime( 2026, 6, 15, 14, 30, 45 ).time()


def Test_FormatTimeValue_TestSecondsPresent_ExpectHmsFormat() -> None:
   assert DateValues.format_time_value( '14:30:45' ) == '14:30:45'


def Test_ScheduleTimeKeyFromSeconds_TestInvalidSeconds_ExpectValueError() -> None:
   with pytest.raises( ValueError ):
      DateValues.schedule_time_key_from_seconds( -1 )


def Test_ScheduleTimeKeyFromMinutes_TestInvalidMinutes_ExpectValueError() -> None:
   with pytest.raises( ValueError ):
      DateValues.schedule_time_key_from_minutes( -5 )


def Test_AddMinutesToTime_TestNonPositiveDuration_ExpectNone() -> None:
   assert DateValues.add_minutes_to_time( '10:00 AM', 0 ) is None
   assert DateValues.add_minutes_to_time( '10:00 AM', -5 ) is None


def Test_NormalizeDateKey_TestInvalidDate_ExpectNone() -> None:
   assert DateValues.normalize_date_key( 'not-a-date' ) is None


def Test_FormatDisplayDateValue_TestValidDate_ExpectMonthDayYear() -> None:
   assert DateValues.format_display_date_value( '2026-06-15' ) == 'June 15, 2026'


def Test_FormatDisplayDateValue_TestInvalidDate_ExpectNone() -> None:
   assert DateValues.format_display_date_value( None ) is None


def Test_FormatTimeValue_TestEmptyTime_ExpectNone() -> None:
   assert DateValues.format_time_value( '' ) is None


def Test_FormatTimeValue_TestWithoutSeconds_ExpectHmFormat() -> None:
   assert DateValues.format_time_value( '14:30' ) == '14:30'


def Test_NormalizeUniqueItineraryScheduleTimes_TestDelegates_ExpectUniqueTimes() -> None:
   assert DateValues.normalize_unique_itinerary_schedule_times(
      [ '10:00 AM', '10:00 AM', '11:00 AM' ] ) == [ '10:00 AM', '11:00 AM' ]


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
   monkeypatch.setattr(
      DateValues,
      'parse_date_value',
      lambda _value: None )

   assert DateValues.normalize_date_key( '2026-06-15' ) is None
