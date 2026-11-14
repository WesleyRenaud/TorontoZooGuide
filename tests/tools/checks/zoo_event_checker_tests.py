from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.models import Event
from tools.checks.check_report import CheckReport
from tools.checks.date_span import DateSpan
from tools.checks.website_zoo_event import WebsiteZooEvent
from tools.checks.zoo_event_checker import ZooEventChecker


TODAY = date( 2026, 11, 13 )


def card(
      name: str,
      href: str,
      card_date: str,
      description: str,
      image: str = '' ) -> str:
   thumbnail = '' if image == '' else f'<img src="{ image }">'
   return (
      '<article class="card-slider-item">'
      f'<a href="{ href }">'
      f'{ thumbnail }'
      f'<h2>{ name }</h2>'
      f'<p class="card-date">{ card_date }</p>'
      f'<p>{ description }</p>'
      '</a></article>'
   )


def home( *cards: str ) -> str:
   return '<h1 id="events">What\'s happening</h1>' + ''.join( cards )


def database( path: Path, events: list[ Event ] ) -> Path:
   connection = sqlite3.connect( path )
   connection.execute(
      """   CREATE TABLE ZooEvent (
               NAME TEXT NOT NULL,
               LOCATION TEXT NOT NULL,
               DESCRIPTION TEXT NOT NULL,
               LINK TEXT NOT NULL,
               START_DATE TEXT NOT NULL,
               END_DATE TEXT,
               PRIMARY KEY (NAME, START_DATE)
            );
      """
   )

   for event in events:
      connection.execute(
         """   INSERT INTO ZooEvent (
                  NAME, LOCATION, DESCRIPTION, LINK, START_DATE, END_DATE
               ) VALUES (?, ?, ?, ?, ?, ?);
         """,
         (
            event.name,
            event.location,
            event.description,
            event.link,
            event.start_date,
            event.end_date,
         ),
      )

   connection.commit()
   connection.close()
   return path


def stored_rows( path: Path ) -> list[ tuple[ str, str, str ] ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      'SELECT NAME, START_DATE, END_DATE FROM ZooEvent ORDER BY NAME;'
   ).fetchall()
   connection.close()
   return rows


def Test_Window_TestCardRange_ExpectThoseDates() -> None:
   found = WebsiteZooEvent.window(
      'Veterans & Military Appreciation Week',
      'Sunday, November 8 Friday, November 13',
      '',
      TODAY,
   )

   assert found == DateSpan( start=date( 2026, 11, 8 ), end=date( 2026, 11, 13 ) )


def Test_Window_TestTitleSpan_ExpectTitleDates() -> None:
   found = WebsiteZooEvent.window(
      'Member Holiday Party - December 12-13 & 19-20',
      'Tickets on Sale Thursday, November 5!',
      '',
      TODAY,
   )

   assert found == DateSpan( start=date( 2026, 12, 12 ), end=date( 2026, 12, 20 ) )


def Test_Window_TestPageSeason_ExpectRolledEnd() -> None:
   found = WebsiteZooEvent.window(
      'Glow In The Wild',
      'Get 20% Off All November Long!',
      'Glow in the Wild runs from September 3 to January 3.',
      TODAY,
   )

   assert found == DateSpan( start=date( 2026, 9, 3 ), end=date( 2027, 1, 3 ) )


def Test_Window_TestCurrentPageRange_ExpectRangeContainingToday() -> None:
   found = WebsiteZooEvent.choose_range(
      'Display Period: April 1, 2027 – April 25, 2027. '
      'Entry Period: October 6, 2026 – December 7, 2026.',
      TODAY,
   )

   assert found == DateSpan( start=date( 2026, 10, 6 ), end=date( 2026, 12, 7 ) )


def Test_Read_TestIndexCard_ExpectSkipped() -> None:
   html = home(
      card( 'See All Upcoming Toronto Zoo Events & Programs', 'https://www.torontozoo.com/events/', '', '' ),
      '<article class="card-slider-item"><a href=""></a></article>',
   )

   assert WebsiteZooEvent.read( html, TODAY, {} ) == []


def Test_Limited_TestLongDescription_ExpectShortenedAtSentence() -> None:
   sentence = (
      'This two-day indoor/outdoor market showcases talented artisans, processors, and producers.'
   )
   description = (
      f'{ sentence } Food, crafts, and holiday gifts from local and surrounding '
      'communities fill the market for the whole family.'
   )

   shortened = WebsiteZooEvent.limited( description )

   assert len( description ) > WebsiteZooEvent.DESCRIPTION_LIMIT
   assert shortened == sentence


def Test_Limited_TestFirstSentenceOverLimit_ExpectThatSentence() -> None:
   sentence = ( 'A' * 170 ) + '.'
   description = f'{ sentence } More follows here.'

   assert WebsiteZooEvent.limited( description ) == sentence


def Test_CheckSchedules_TestUnreadableDates_ExpectReportedAndKept(
      tmp_path: Path ) -> None:
   path = database( tmp_path / 'animals.db', [
      Event(
         'Glow In The Wild',
         '',
         'Stored description',
         'https://www.torontozoo.com/glow',
         '2026-09-02',
         '2027-01-03',
      ),
   ] )
   html = home(
      card(
         'Glow In The Wild',
         'https://www.torontozoo.com/glowinthewild',
         'Get 20% Off All November Long!',
         'Journey Through an Illuminated Animal Lantern Experience!',
      ),
      card(
         'Rain Barrel Art Project - Season 3',
         'https://www.torontozoo.com/rainbarrel',
         'Submissions Open Now!',
         'Calling all students.',
      ),
   )
   CheckReport.reset_fixed_count()

   issues = ZooEventChecker.check_schedules( path, TODAY, html, {} )

   assert issues == 1
   assert CheckReport.fixed_count == 0
   assert stored_rows( path ) == [
      ( 'Glow In The Wild', '2026-09-02', '2027-01-03' ),
   ]


def Test_CheckSchedules_TestMissingAndExtra_ExpectAddedAndRemoved(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   path = database( tmp_path / 'animals.db', [
      Event(
         'Glow in the Wild',
         '',
         'Stored description',
         'https://www.torontozoo.com/glow',
         '2026-09-02',
         '2027-01-03',
      ),
      Event(
         'Member Mondays',
         '',
         'Mondays',
         'https://www.torontozoo.com/membermondays',
         '2026-08-02',
         '2026-08-31',
      ),
   ] )
   html = home(
      card(
         'Glow In The Wild',
         'https://www.torontozoo.com/glowinthewild',
         'September 3 to January 3',
         'Journey Through an Illuminated Animal Lantern Experience!',
         '/!/img/event/26/glowthumb1080n.webp',
      ),
      card(
         'Veterans & Military Appreciation Week',
         'https://www.torontozoo.com/events/veteran#evt',
         'Sunday, November 8<br>Friday, November 13',
         'Complimentary admission.',
      ),
   )
   CheckReport.reset_fixed_count()

   issues = ZooEventChecker.check_schedules( path, TODAY, html, {} )
   output = capsys.readouterr().out

   assert issues == 0
   assert CheckReport.fixed_count == 3
   assert 'Photo: https://www.torontozoo.com/!/img/event/26/glowthumb1080n.webp' in output
   assert 'Journey Through an Illuminated Animal Lantern Experience!' in output
   assert stored_rows( path ) == [
      ( 'Glow In The Wild', '2026-09-03', '2027-01-03' ),
      ( 'Member Mondays', '2026-08-02', '2026-08-31' ),
      ( 'Veterans & Military Appreciation Week', '2026-11-08', '2026-11-13' ),
   ]
