from __future__ import annotations

import pytest

from tools.checks.attraction_hours_reader import AttractionHoursReader


def _card( title: str, status: str, extra: str = '' ) -> str:
   return (
      f'<a class="col3" href="/tz/{ title }">'
      f'<div class="col3title">{ title }</div>'
      f'<span class="opentxt">{ status }</span>{ extra }</a>'
   )


def Test_Parse_TestLabeledWeekdayAndWeekend_ExpectBothPairs() -> None:
   card = _card(
      'Zoomobile',
      'Open Daily',
      '<strong>Weekdays: 10:00am - 4:00pm Weekends/Holidays: 10:00am - 5:30pm</strong>',
   )
   hours = AttractionHoursReader.parse( card, card )

   assert hours != None
   assert hours.weekday_opens == '10:00 AM'
   assert hours.weekday_closes == '4:00 PM'
   assert hours.weekend_opens == '10:00 AM'
   assert hours.weekend_closes == '5:30 PM'


def Test_Parse_TestFridayAndWeekend_ExpectFridayOnWeekdays() -> None:
   card = _card(
      'TundraAir Ride',
      'Open Fridays/Weekends/Holidays',
      '<strong>Fridays: 11:00am - 4:30pm Weekends/Holidays: 11:00am - 6:00pm</strong>',
   )
   hours = AttractionHoursReader.parse( card, card )

   assert hours != None
   assert hours.weekday_opens == '11:00 AM'
   assert hours.weekday_closes == '4:30 PM'
   assert hours.weekend_opens == '11:00 AM'
   assert hours.weekend_closes == '6:00 PM'


def Test_Parse_TestWeekdaysAfterFriday_ExpectWeekdayLabel() -> None:
   card = _card(
      'TundraAir Ride',
      'Open Daily',
      '<strong>Fridays: 11:00am - 4:30pm Weekdays: 10:00am - 6:00pm</strong>',
   )
   hours = AttractionHoursReader.parse( card, card )

   assert hours != None
   assert hours.weekday_opens == '10:00 AM'
   assert hours.weekday_closes == '6:00 PM'


def Test_Parse_TestSingleWeekendSpan_ExpectWeekendOnly() -> None:
   card = _card(
      'Splash Island',
      'Open Weekends Until September 29',
      '<strong>11:00am - 5:00pm</strong>',
   )
   hours = AttractionHoursReader.parse( card, card )

   assert hours != None
   assert hours.weekday_opens == None
   assert hours.weekend_opens == '11:00 AM'
   assert hours.weekend_closes == '5:00 PM'


def Test_Parse_TestSingleDailySpan_ExpectBothPairs() -> None:
   card = _card(
      'Splash Island',
      'Open Daily',
      '<strong>10:30am - 6:00pm</strong>',
   )
   hours = AttractionHoursReader.parse( card, card )

   assert hours != None
   assert hours.weekday_opens == '10:30 AM'
   assert hours.weekday_closes == '6:00 PM'
   assert hours.weekend_opens == '10:30 AM'
   assert hours.weekend_closes == '6:00 PM'


def Test_Parse_TestWordTo_ExpectWeekendSpan() -> None:
   card = _card(
      'Gorilla Climb Ropes Course',
      'Open Weekends/Holidays',
      '<strong>11:00am to 6:00pm</strong>',
   )
   hours = AttractionHoursReader.parse( card, card )

   assert hours != None
   assert hours.weekday_opens == None
   assert hours.weekend_opens == '11:00 AM'
   assert hours.weekend_closes == '6:00 PM'


def Test_Parse_TestDuringZooHours_ExpectHeaderPairs() -> None:
   card = _card( 'Kids Zoo', 'Open Daily', '<strong>During Zoo Hours</strong>' )
   page = 'Weekdays: 9:30am - 4:30pm Weekends: 9:30am - 6:00pm' + card
   hours = AttractionHoursReader.parse( card, page )

   assert hours != None
   assert hours.weekday_opens == '9:30 AM'
   assert hours.weekday_closes == '4:30 PM'
   assert hours.weekend_opens == '9:30 AM'
   assert hours.weekend_closes == '6:00 PM'


def Test_Parse_TestDailyHeader_ExpectBothPairs() -> None:
   card = _card( 'Greenhouse', 'Open Daily', '<strong>During Zoo Hours</strong>' )
   page = 'Daily 9:30am – 4:30pm' + card
   hours = AttractionHoursReader.parse( card, page )

   assert hours != None
   assert hours.weekday_opens == '9:30 AM'
   assert hours.weekday_closes == '4:30 PM'
   assert hours.weekend_opens == '9:30 AM'
   assert hours.weekend_closes == '4:30 PM'


def Test_Parse_TestWeatherPermitting_ExpectNoHours() -> None:
   card = _card( 'Zoomobile', 'Open Daily', '<strong>Weather Permitting</strong>' )

   assert AttractionHoursReader.parse( card, card ) == None


def Test_Parse_TestTimesMayVary_ExpectNoHours() -> None:
   card = _card(
      'Kangaroo Walk-Thru',
      'Open Weekends & Holidays',
      '<strong>Times May Vary</strong>',
   )

   assert AttractionHoursReader.parse( card, card ) == None


def Test_Parse_TestCommentedHours_ExpectNoHours() -> None:
   card = _card(
      'Splash Island',
      'Open Daily',
      '<!-- <b>10:30am - 6:00pm</b> --><strong>Weather Permitting</strong>',
   )

   assert AttractionHoursReader.parse( card, card ) == None


def Test_Parse_TestClosedForTheSeason_ExpectNoHours() -> None:
   card = _card(
      'Splash Island',
      'Closed for the Season',
      '<strong>10:30am - 6:00pm</strong>',
   )

   assert AttractionHoursReader.parse( card, card ) == None


def Test_Parse_TestWeekendStatusOnDescription_ExpectWeekendOnly() -> None:
   description = '<strong>10:00am - 4:30pm</strong><strong>Weather Permitting</strong>'
   hours = AttractionHoursReader.parse(
      description,
      description,
      'Open Weekends & Holidays',
   )

   assert hours != None
   assert hours.weekday_opens == None
   assert hours.weekend_opens == '10:00 AM'
   assert hours.weekend_closes == '4:30 PM'


def Test_Parse_TestClockWithoutSpace_ExpectHours() -> None:
   description = '<strong>10:00am-4:00pm</strong>'
   hours = AttractionHoursReader.parse( description, description, 'Open Weekends & Holidays' )

   assert hours != None
   assert hours.weekend_opens == '10:00 AM'
   assert hours.weekend_closes == '4:00 PM'


def Test_Published_TestTourDescription_ExpectWeekendHours( monkeypatch: pytest.MonkeyPatch ) -> None:
   def tour_description( cls: type, href: str ) -> str:
      return '<strong>10:00am - 4:30pm</strong><strong>Weather Permitting</strong>'

   monkeypatch.setattr(
      AttractionHoursReader,
      'tour_description',
      classmethod( tour_description ),
   )
   card = _card(
      'Conservation Carousel',
      'Open Weekends & Holidays',
      '<strong>Weather Permitting</strong>',
   )
   hours = AttractionHoursReader.published( card, card, '/tickets/carousel' )

   assert hours != None
   assert hours.weekday_opens == None
   assert hours.weekend_opens == '10:00 AM'
   assert hours.weekend_closes == '4:30 PM'
