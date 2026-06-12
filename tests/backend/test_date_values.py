from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime

import pytest

from api.shared.date_values import DateValues
from api.shared.duration_values import normalize_duration_minutes
from api.shared.duration_values import normalize_duration_seconds
from api.types import DateInput, DateKey


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
def test_parse_date_value( value: DateInput, expected: date | None ) -> None:
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
def test_normalize_date_key( value: DateInput, expected: DateKey | None ) -> None:
   assert DateValues.normalize_date_key( value ) == expected


def test_normalize_date_key_returns_none_for_unsupported_date_strings() -> None:
   assert DateValues.normalize_date_key( 'June 15, 2026' ) is None


def test_resolve_open_ended_date_range_keeps_open_end_date() -> None:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date='2026-06-01',
      end_date=None )

   assert date_range.start_date == '2026-06-01'
   assert date_range.end_date is None


def test_resolve_open_ended_date_range_uses_today_for_missing_start(
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

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
def test_parse_datetime_value( value: str | None, expected: datetime | None ) -> None:
   assert DateValues.parse_datetime_value( value ) == expected


def test_parse_values_raise_for_unsupported_formats() -> None:
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
      ( '1:00 PM', '13:00' ),
      ( '13:45', '13:45' ),
      ( '13:45:30', '13:45:30' ),
      ( '10:00', '10:00' ),
      ( 'not-a-time', None ),
   ]
)
def test_normalize_itinerary_schedule_time(
      value: str | None,
      expected: str | None ) -> None:
   assert DateValues.normalize_itinerary_schedule_time( value ) == expected


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
def test_normalize_schedule_time_key(
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
def test_time_value_in_seconds(
      value: str | None,
      expected: int | None ) -> None:
   assert DateValues.time_value_in_seconds( value ) == expected


@pytest.mark.parametrize(
   'total_seconds, expected',
   [
      ( 9 * 3600 + 30 * 60, '09:30' ),
      ( 9 * 3600 + 30 * 60 + 30, '09:30:30' ),
   ]
)
def test_schedule_time_key_from_seconds(
      total_seconds: int,
      expected: str ) -> None:
   assert DateValues.schedule_time_key_from_seconds( total_seconds ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( 0, None ),
      ( 7.2, 8 ),
      ( 8, 8 ),
      ( 20, 20 ),
   ]
)
def test_normalize_duration_minutes( value: float | None, expected: int | None ) -> None:
   assert normalize_duration_minutes( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( 0, None ),
      ( 0.5, 30 ),
      ( 7.2, 432 ),
      ( 8, 480 ),
      ( 20, 1200 ),
   ]
)
def test_normalize_duration_seconds( value: float | None, expected: int | None ) -> None:
   assert normalize_duration_seconds( value ) == expected


@pytest.mark.parametrize(
   'left, right, expected',
   [
      ( date( 2026, 6, 15 ), None, True ),
      ( date( 2026, 6, 15 ), '2026-06-15', True ),
      ( date( 2026, 6, 14 ), '2026-06-15', False ),
      ( date( 2026, 6, 16 ), '2026-06-14', True ),
   ]
)
def test_is_date_on_or_after( left: date, right: DateInput, expected: bool ) -> None:
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
def test_is_date_on_or_before( left: date, right: DateInput, expected: bool ) -> None:
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
def test_is_date_in_range(
      target: date,
      start: DateInput,
      end: DateInput,
      expected: bool ) -> None:
   assert DateValues.is_date_in_range( target_date=target, start_date_value=start, end_date_value=end ) is expected
