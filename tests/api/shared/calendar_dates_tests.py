from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Any

import pytest

from api.shared.calendar_dates import CalendarDates
import api.shared.date_values as date_values
from api.types import Types


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '', None ),
      ( 1, 1 ),
      ( 12, 12 ),
      ( 0, None ),
      ( 13, None ),
      ( '1', None ),
      ( 'January', 1 ),
      ( 'Jan', 1 ),
      ( 'JAN', 1 ),
      ( 'February', 2 ),
      ( 'Feb', 2 ),
      ( 'FEB', 2 ),
      ( 'March', 3 ),
      ( 'Mar', 3 ),
      ( 'MAR', 3 ),
      ( 'April', 4 ),
      ( 'Apr', 4 ),
      ( 'APR', 4 ),
      ( 'May', 5 ),
      ( 'MAY', 5 ),
      ( 'June', 6 ),
      ( 'Jun', 6 ),
      ( 'JUN', 6 ),
      ( 'July', 7 ),
      ( 'Jul', 7 ),
      ( 'JUL', 7 ),
      ( 'August', 8 ),
      ( 'Aug', 8 ),
      ( 'AUG', 8 ),
      ( 'September', 9 ),
      ( 'Sep', 9 ),
      ( 'SEP', 9 ),
      ( 'October', 10 ),
      ( 'Oct', 10 ),
      ( 'OCT', 10 ),
      ( 'November', 11 ),
      ( 'Nov', 11 ),
      ( 'NOV', 11 ),
      ( 'December', 12 ),
      ( 'Dec', 12 ),
      ( 'DEC', 12 ),
      ( 'december', None ),
      ( 'NotAMonth', None ),
   ]
)
def Test_normalize_month( value: Types.MonthInput, expected: Types.VisitMonth | None ) -> None:
   month = CalendarDates.normalize_month( value )

   assert month == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( 1, 'Jan' ),
      ( 12, 'Dec' ),
      ( '1', 'Jan' ),
      ( '12', 'Dec' ),
      ( 'January', 'Jan' ),
      ( 'sept', 'Sep' ),
      ( 'DECEMBER', 'Dec' ),
   ]
)
def Test_get_month_abbreviation( value: Types.MonthInput, expected: str ) -> None:
   abbreviation = CalendarDates.get_month_abbreviation( value )

   assert abbreviation == expected


@pytest.mark.parametrize(
   'value',
   [
      0,
      13,
      '13',
      'NotAMonth',
      [],
   ]
)
def Test_get_month_abbreviation_rejects_invalid_values( value: Any ) -> None:
   with pytest.raises( ValueError ):
      CalendarDates.get_month_abbreviation( value )


@pytest.mark.parametrize(
   'value, expected',
   [
      ( 1, 1 ),
      ( 6, 6 ),
      ( '06', 6 ),
      ( 'June', 6 ),
      ( 'JUN', 6 ),
      ( 'January', 1 ),
      ( 'december', 12 ),
   ]
)
def Test_resolve_visit_calendar_month(
      value: Types.MonthInput,
      expected: Types.VisitMonth ) -> None:
   month = CalendarDates.resolve_visit_calendar_month( value )

   assert month == expected
   assert isinstance( month, int )


def Test_ResolveVisitCalendarMonth_TestInvalidValues_ExpectRaises() -> None:
   month = 13

   with pytest.raises( ValueError ):
      CalendarDates.resolve_visit_calendar_month( month )


def Test_ResolveVisitDayOfMonth_TestStringDay_ExpectDayNumber() -> None:
   day = '15'

   resolved_day = CalendarDates.resolve_visit_day_of_month( day )

   assert resolved_day == int( day )


def Test_ResolveVisitDayOfMonth_TestIntegerDay_ExpectSame() -> None:
   day = 7

   resolved_day = CalendarDates.resolve_visit_day_of_month( day )

   assert resolved_day == day


def Test_ResolveVisitCalendarYear_TestExplicitYear_ExpectValue() -> None:
   year = 2029

   resolved_year = CalendarDates.resolve_visit_calendar_year( year )

   assert resolved_year == year


def Test_ResolveVisitCalendarYear_TestNone_ExpectModuleDatetime( monkeypatch: pytest.MonkeyPatch ) -> None:
   class Fixed( datetime ):
      @classmethod
      def now( cls, tz: datetime.tzinfo | None = None ) -> datetime:
         return datetime( 2032, 3, 1, 0, 0, 0 )

   monkeypatch.setattr( date_values, 'datetime', Fixed )

   year = CalendarDates.resolve_visit_calendar_year( None )

   assert year == Fixed.now().year


def Test_VisitTargetDate_TestMonthName_ExpectDate() -> None:
   month = 'June'
   day = 15
   year = 2026

   target = CalendarDates.visit_target_date( month, day, year )

   assert target == date(
      year,
      CalendarDates.resolve_visit_calendar_month( month ),
      day )


def Test_VisitTargetDate_TestMonthNumber_ExpectDate() -> None:
   month = 6
   day = 15
   year = 2026

   target = CalendarDates.visit_target_date( month, day, year )

   assert target == date( year, month, day )


def Test_VisitTargetDate_TestStringYear_ExpectDate() -> None:
   month = 'January'
   day = 10
   year = '2028'

   target = CalendarDates.visit_target_date( month, day, year )

   assert target == date(
      int( year ),
      CalendarDates.resolve_visit_calendar_month( month ),
      day )


def Test_ScheduleIncludesWeekday_TestMonday_ExpectFlagValue() -> None:
   flags = ( True, False, False, False, False, False, False )
   monday = 0

   included = CalendarDates.schedule_includes_weekday( monday, flags )

   assert included is flags[ monday ]


def Test_ScheduleIncludesWeekday_TestTuesday_ExpectFlagValue() -> None:
   flags = ( True, False, False, False, False, False, False )
   tuesday = 1

   included = CalendarDates.schedule_includes_weekday( tuesday, flags )

   assert included is flags[ tuesday ]


def Test_ScheduleIncludesWeekday_TestNegativeIndex_ExpectFalse() -> None:
   flags = ( True, ) * 7
   weekday_index = -1

   included = CalendarDates.schedule_includes_weekday( weekday_index, flags )

   assert included is False


def Test_ScheduleIncludesWeekday_TestIndexPastSunday_ExpectFalse() -> None:
   flags = ( True, ) * 7
   weekday_index = 7

   included = CalendarDates.schedule_includes_weekday( weekday_index, flags )

   assert included is False


@pytest.mark.parametrize(
   'month, day',
   [
      ( 'JAN', 1 ),
      ( 'FEB', 1 ),
      ( 'MAR', 1 ),
      ( 'APR', 15 ),
      ( 'JUN', 15 ),
      ( 'DEC', 31 ),
   ]
)
def Test_get_day_of_year( month: str, day: int ) -> None:
   year = 2026

   day_of_year = CalendarDates.get_day_of_year( month, day )

   assert day_of_year == date(
      year,
      CalendarDates.resolve_visit_calendar_month( month ),
      day ).timetuple().tm_yday - 1


def Test_GetDayOfYear_TestInvalidMonth_ExpectKeyError() -> None:
   month = 'NotAMonth'

   with pytest.raises( KeyError ):
      CalendarDates.get_day_of_year( month, 1 )


@pytest.mark.parametrize(
   'month, expected',
   [
      ( 'Jan', 'Feb' ),
      ( 'JAN', 'Feb' ),
      ( 'Feb', 'Mar' ),
      ( 'MAR', 'Apr' ),
      ( 'Apr', 'May' ),
      ( 'MAY', 'Jun' ),
      ( 'Jun', 'Jul' ),
      ( 'JUL', 'Aug' ),
      ( 'Aug', 'Sep' ),
      ( 'SEP', 'Oct' ),
      ( 'Oct', 'Nov' ),
      ( 'NOV', 'Dec' ),
      ( 'Dec', 'Jan' ),
      ( 'DEC', 'Jan' ),
      ( 'BadMonth', None ),
   ]
)
def Test_get_next_month( month: str, expected: str | None ) -> None:
   next_month = CalendarDates.get_next_month( month )

   assert next_month == expected


@pytest.mark.parametrize(
   'month, expected',
   [
      ( 'JAN', 31 ),
      ( 'Jan', 31 ),
      ( 'MAR', 31 ),
      ( 'APR', 30 ),
      ( 'Apr', 30 ),
      ( 'JUN', 30 ),
      ( 'SEP', 30 ),
      ( 'NOV', 30 ),
      ( 'FEB', 28 ),
      ( 'Feb', 28 ),
      ( 'BadMonth', None ),
   ]
)
def Test_get_number_of_days_in_month( month: str, expected: int | None ) -> None:
   days = CalendarDates.get_number_of_days_in_month( month )

   assert days == expected


@pytest.mark.parametrize(
   'month, expected',
   [
      ( 5, True ),
      ( 6, True ),
      ( 10, True ),
      ( 'May', True ),
      ( 'October', True ),
      ( 4, False ),
      ( 11, False ),
      ( 'April', False ),
      ( 'November', False ),
   ]
)
def Test_is_peak_season_month( month: Types.MonthInput, expected: bool ) -> None:
   is_peak = CalendarDates.is_peak_season_month( month )

   assert is_peak is expected


def Test_GetEasterDate_TestYear2026_ExpectAprilFifth() -> None:
   year = 2026

   easter = CalendarDates.get_easter_date( year )

   assert easter == date( year, 4, 5 )


def Test_GetFamilyDay_TestYear2026_ExpectThirdMondayInFebruary() -> None:
   year = 2026

   family_day = CalendarDates.get_family_day( year )

   assert family_day == date( year, 2, 16 )


def Test_GetGoodFriday_TestYear2026_ExpectTwoDaysBeforeEaster() -> None:
   year = 2026

   good_friday = CalendarDates.get_good_friday( year )

   assert good_friday == CalendarDates.get_easter_date( year ) - timedelta( days=2 )


def Test_GetVictoriaDay_TestYear2026_ExpectMondayBeforeMay24() -> None:
   year = 2026

   victoria_day = CalendarDates.get_victoria_day( year )

   assert victoria_day == date( year, 5, 18 )


def Test_GetCivicHoliday_TestYear2026_ExpectFirstMondayInAugust() -> None:
   year = 2026

   civic_holiday = CalendarDates.get_civic_holiday( year )

   assert civic_holiday == date( year, 8, 3 )


def Test_GetLabourDay_TestYear2026_ExpectFirstMondayInSeptember() -> None:
   year = 2026

   labour_day = CalendarDates.get_labour_day( year )

   assert labour_day == date( year, 9, 7 )


def Test_GetThanksgiving_TestYear2026_ExpectSecondMondayInOctober() -> None:
   year = 2026

   thanksgiving = CalendarDates.get_thanksgiving( year )

   assert thanksgiving == date( year, 10, 12 )


def Test_IsHoliday_TestCanadianHolidays_ExpectTrue() -> None:
   year = 2026
   holidays = [
      date( year, 1, 1 ),
      CalendarDates.get_family_day( year ),
      CalendarDates.get_good_friday( year ),
      CalendarDates.get_victoria_day( year ),
      date( year, 7, 1 ),
      CalendarDates.get_civic_holiday( year ),
      CalendarDates.get_labour_day( year ),
      CalendarDates.get_thanksgiving( year ),
      date( year, 12, 25 ),
   ]

   results = [ CalendarDates.is_holiday( holiday ) for holiday in holidays ]

   assert all( results )


def Test_IsHoliday_TestChristmasEve_ExpectFalse() -> None:
   christmas_eve = date( 2026, 12, 24 )

   is_holiday = CalendarDates.is_holiday( christmas_eve )

   assert is_holiday is False


def Test_IsHoliday_TestMidJune_ExpectFalse() -> None:
   mid_june = date( 2026, 6, 15 )

   is_holiday = CalendarDates.is_holiday( mid_june )

   assert is_holiday is False


def Test_NextWeekdayDate_TestFromSaturday_ExpectMonday() -> None:
   saturday = date( 2026, 6, 20 )

   next_weekday = CalendarDates.next_weekday_date( saturday )

   assert next_weekday.weekday() < 5
   assert CalendarDates.is_holiday( next_weekday ) is False
   assert next_weekday > saturday


def Test_NextWeekdayDate_TestFromMonday_ExpectSameDate() -> None:
   monday = date( 2026, 6, 15 )

   next_weekday = CalendarDates.next_weekday_date( monday )

   assert next_weekday == monday


def Test_NextWeekendOrHolidayDate_TestFromWeekday_ExpectWeekendOrHoliday() -> None:
   weekday = date( 2026, 6, 15 )

   next_date = CalendarDates.next_weekend_or_holiday_date( weekday )

   assert CalendarDates.is_weekend_or_holiday( next_date )
   assert next_date >= weekday


def Test_NextWeekendOrHolidayDate_TestFromSaturday_ExpectSameDate() -> None:
   saturday = date( 2026, 6, 20 )

   next_date = CalendarDates.next_weekend_or_holiday_date( saturday )

   assert next_date == saturday


def Test_NextWeekendOrHolidayDate_TestFromHoliday_ExpectSameDate() -> None:
   canada_day = date( 2026, 7, 1 )

   next_date = CalendarDates.next_weekend_or_holiday_date( canada_day )

   assert next_date == canada_day


def Test_ResolveVisitCalendarMonth_TestNormalizeReturnsNone_ExpectValueError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      CalendarDates,
      'normalize_month',
      lambda **kwargs: None )

   with pytest.raises( ValueError, match='Invalid month' ):
      CalendarDates.resolve_visit_calendar_month( 'June' )
