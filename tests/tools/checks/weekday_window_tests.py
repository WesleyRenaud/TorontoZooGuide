from __future__ import annotations

from tools.checks.weekday_window import WeekdayWindow


def Test_Parse_TestOpenDaily_ExpectEveryDay() -> None:
   window = WeekdayWindow.parse( 'Open Daily' )

   assert window == WeekdayWindow( frozenset( range( 7 ) ), False )


def Test_Parse_TestWeekendsAndHolidays_ExpectWeekendHolidays() -> None:
   window = WeekdayWindow.parse( 'Open Weekends & Holidays' )

   assert window == WeekdayWindow( frozenset( { 5, 6 } ), True )


def Test_Parse_TestWeekends_ExpectSaturdayAndSunday() -> None:
   assert WeekdayWindow.parse( 'Weekends' ) == WeekdayWindow( frozenset( { 5, 6 } ), False )
   assert WeekdayWindow.parse( 'Open Weekends' ) == WeekdayWindow( frozenset( { 5, 6 } ), False )


def Test_Parse_TestThursdayToSunday_ExpectThoseDays() -> None:
   window = WeekdayWindow.parse( 'Thursday to Sunday' )

   assert window == WeekdayWindow( frozenset( { 3, 4, 5, 6 } ), False )


def Test_Parse_TestFridayToMonday_ExpectWrappedDays() -> None:
   window = WeekdayWindow.parse( 'Friday to Monday' )

   assert window == WeekdayWindow( frozenset( { 4, 5, 6, 0 } ), False )


def Test_Parse_TestClosedForSeason_ExpectNoWindow() -> None:
   assert WeekdayWindow.parse( 'Closed for the Season' ) == None
   assert WeekdayWindow.parse( 'Closed For The Season' ) == None


def Test_WeekendOnly_TestOpenDaily_ExpectWeekdayMonths() -> None:
   pattern = WeekdayWindow.parse( 'Open Daily' )

   assert pattern.weekend_only() == False


def Test_WeekendOnly_TestThursdayToSunday_ExpectWeekdayMonths() -> None:
   pattern = WeekdayWindow.parse( 'Thursday to Sunday' )

   assert pattern.weekend_only() == False


def Test_WeekendOnly_TestOpenWeekends_ExpectWeekendMonths() -> None:
   pattern = WeekdayWindow.parse( 'Open Weekends' )

   assert pattern.weekend_only() == True


def Test_WeekendOnly_TestWeekendsAndHolidays_ExpectWeekendMonths() -> None:
   pattern = WeekdayWindow.parse( 'Open Weekends & Holidays' )

   assert pattern.weekend_only() == True


def Test_Parse_TestSpecialProgramme_ExpectNoWindow() -> None:
   assert WeekdayWindow.parse( 'Open During Glow in the Wild' ) == None
   assert WeekdayWindow.parse( None ) == None
