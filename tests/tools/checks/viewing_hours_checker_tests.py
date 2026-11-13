from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from tools.checks.animal_catalogue import AnimalCatalogue
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.paths import Paths
from tools.checks.viewing_hours_checker import ViewingHoursChecker
from tools.checks.website_page import WebsitePage


TODAY = date( 2026, 11, 12 )
HORIZON = CalendarDates.one_month_later( TODAY )
HIPPO = 'Pygmy Hippopotamus'
PAVILION = 'African Rainforest Pavilion'
GORILLA = 'Western Lowland Gorilla'
OTTER = 'North American River Otter'
AMERICAS = 'Americas Pavilion'
WOMBAT = 'Southern Hairy-Nosed Wombat'
AUSTRALASIA = 'Australasia Pavilion'
CAMEL = 'Bactrian Camel'
EURASIA = 'Eurasia Wilds'
GIRAFFE = 'Masai Giraffe'
SAVANNA = 'Africa Savanna'
KEPT = 'Keep this message.'

SCHEMA = """
CREATE TABLE Enclosure (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL
);

CREATE TABLE AnimalVisibilitySchedule (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   SCHEDULE_START_DATE  TEXT,
   SCHEDULE_END_DATE    TEXT,
   DAILY_START_TIME     TEXT,
   DAILY_END_TIME       TEXT,
   VIEWING_MESSAGE      TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""

HOME = """
<div class="mySlides"><a href="/maple">Maple</a></div>
<div class="mySlides"><a href="https://example.com/outside">Outside</a></div>
<article class="card-slider-item"><a href="/giraffe">Giraffe</a></article>
<article class="card-slider-item"><a href="/animals">Animals</a></article>
"""

ANIMALS = """
<div class="pgbut custom">
<a href="/maple">Maple</a>
<a href="/giraffe">Giraffe</a>
<a href="/animals/North%20American%20River%20Otter">Otter</a>
<a href="/wombat">Wombat</a>
<a href="/camel">Camel</a>
</div>
<a href="/alerts">Alerts</a>
<div class="pgbut"><a href="/animals/africa">Africa</a></div>
"""

MAPLE = """
<h1>Daily from 10:30am - 2:30pm *, come meet the newest addition in the African Rainforest Pavilion.</h1>
<p>As baby Maple continues to adjust, she or her mother Kindia may not always be visible.</p>
<p>The Western Lowland Gorilla lives nearby.</p>
<a href="/animals/Pygmy%20hippopotamus">Learn More About Pygmy Hippopotamus</a>
"""

GIRAFFE_PAGE = '<h1>Come and meet Imara in the Africa Savanna.</h1>'

OTTER_PAGE = '<h1>Daily from 10:00am - 1:00pm in the Americas Pavilion.</h1>'

WOMBAT_PAGE = """
<h1>Daily from 9:00am - 11:00am in the Australasia Pavilion.</h1>
<a href="/animals/Southern%20hairy-nosed%20wombat">Learn More</a>
"""

CAMEL_PAGE = """
<h1>Daily from 10:00am - 2:00pm in Eurasia Wilds.</h1>
<a href="/animals/Bactrian%20camel">Learn More</a>
"""

QUIET_ANIMALS = '<div class="pgbut custom"><a href="/wombat">Wombat</a></div>'


def _database( folder: Path ) -> Path:
   database = folder / 'animals.db'
   connection = sqlite3.connect( database )
   connection.executescript( SCHEMA )
   connection.commit()
   connection.close()
   return database


def _insert_enclosure( database: Path, species: str, exhibit: str ) -> None:
   connection = sqlite3.connect( database )
   connection.execute(
      'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES ( ?, ? );',
      ( species, exhibit ),
   )
   connection.commit()
   connection.close()


def _insert_schedule(
      database: Path,
      species: str,
      exhibit: str,
      start: str | None,
      end: str | None,
      opens: str,
      closes: str,
      message: str ) -> None:
   connection = sqlite3.connect( database )
   connection.execute(
      """   INSERT INTO AnimalVisibilitySchedule (
               SPECIES,
               EXHIBIT,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               DAILY_START_TIME,
               DAILY_END_TIME,
               VIEWING_MESSAGE
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      ( species, exhibit, start, end, opens, closes, message ),
   )
   connection.commit()
   connection.close()


def _fetch( pages: dict[ str, str ], url: str ) -> str:
   if url not in pages:
      raise RuntimeError( url )

   return pages[ url ]


def _guest_message( species: str, opens: str, closes: str ) -> str:
   return AppStringProvider.format(
      'guestStatus.animals.limitedViewingScheduleUntil',
      species=species,
      dailyStartTime=opens,
      dailyEndTime=closes,
      endDate=DateValues.format_display_date_value( HORIZON ),
   )


def _featured_pages() -> dict[ str, str ]:
   return {
      WebsitePage.url( '' ): HOME,
      WebsitePage.url( AnimalCatalogue.PAGE ): ANIMALS,
      WebsitePage.url( 'maple' ): MAPLE,
      WebsitePage.url( 'giraffe' ): GIRAFFE_PAGE,
      WebsitePage.url( 'animals/North American River Otter' ): OTTER_PAGE,
      WebsitePage.url( 'wombat' ): WOMBAT_PAGE,
      WebsitePage.url( 'camel' ): CAMEL_PAGE,
   }


def Test_CheckSchedules_TestFeaturedHours_ExpectMonthAligned(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = _database( tmp_path )
   _insert_enclosure( database, HIPPO, PAVILION )
   _insert_enclosure( database, GORILLA, PAVILION )
   _insert_enclosure( database, OTTER, AMERICAS )
   _insert_enclosure( database, WOMBAT, AUSTRALASIA )
   _insert_enclosure( database, CAMEL, EURASIA )
   _insert_enclosure( database, GIRAFFE, SAVANNA )
   _insert_schedule(
      database,
      HIPPO,
      PAVILION,
      '2026-10-20',
      None,
      '10:30 AM',
      '2:30 PM',
      'Baby pygmy hippopotamus Maple is viewable daily.',
   )
   _insert_schedule(
      database,
      GIRAFFE,
      SAVANNA,
      '2026-11-01',
      '2026-12-01',
      '11:00 AM',
      '1:00 PM',
      'Giraffe hours.',
   )
   _insert_schedule(
      database,
      WOMBAT,
      AUSTRALASIA,
      '2026-11-01',
      HORIZON.isoformat(),
      '9:00 AM',
      '11:00 AM',
      KEPT,
   )
   _insert_schedule(
      database,
      CAMEL,
      EURASIA,
      '2026-11-01',
      '2026-11-20',
      '10:00 AM',
      '2:00 PM',
      'Camel hours.',
   )
   pages = _featured_pages()
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: _fetch( pages, url ),
   )
   before = CheckReport.fixed_count

   result = ViewingHoursChecker.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.fixed_count - before == 4
   assert CheckReport.category_line( 'checks.websiteOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.appOnly', 1 ) in output
   assert CheckReport.category_line( 'checks.windowsDoNotAlign', 2 ) in output
   assert 'Set the viewing hours.' in output
   assert 'Removed the viewing hours.' in output
   assert 'Extended the viewing hours.' in output
   assert 'Trimmed the viewing hours.' in output
   assert _guest_message( 'baby pygmy hippopotamus Maple', '10:30 AM', '2:30 PM' ) in output
   assert _guest_message( OTTER, '10:00 AM', '1:00 PM' ) in output
   assert _guest_message( CAMEL, '10:00 AM', '2:00 PM' ) in output
   assert GIRAFFE in output
   assert OTTER in output
   assert WOMBAT not in output
   photo = AnimalDetailImage.source( PAVILION, HIPPO )

   if ( Paths.ROOT / photo ).is_file():
      assert photo in output

   connection = DatabaseConnectionProvider.open( str( database ) )
   RequestConnectionProvider.set( connection )

   try:
      rows = {
         item.species: item
         for item in AnimalCoordinator.get_animal_visibility_schedules()
      }
   finally:
      RequestConnectionProvider.clear()
      connection.close()

   assert set( rows ) == { HIPPO, OTTER, WOMBAT, CAMEL }
   assert rows[ HIPPO ].start_date == '2026-10-20'
   assert rows[ HIPPO ].end_date == HORIZON.isoformat()
   assert rows[ HIPPO ].daily_start_time == '10:30 AM'
   assert rows[ HIPPO ].daily_end_time == '2:30 PM'
   assert rows[ HIPPO ].message == _guest_message(
      'baby pygmy hippopotamus Maple',
      '10:30 AM',
      '2:30 PM',
   )
   assert rows[ OTTER ].start_date == TODAY.isoformat()
   assert rows[ OTTER ].end_date == HORIZON.isoformat()
   assert rows[ OTTER ].message == _guest_message( OTTER, '10:00 AM', '1:00 PM' )
   assert rows[ CAMEL ].start_date == '2026-11-01'
   assert rows[ CAMEL ].end_date == HORIZON.isoformat()
   assert rows[ CAMEL ].message == _guest_message( CAMEL, '10:00 AM', '2:00 PM' )
   assert rows[ WOMBAT ].message == KEPT
   assert rows[ WOMBAT ].end_date == HORIZON.isoformat()


def Test_CheckSchedules_TestMonthAlreadyMatches_ExpectMessageKept(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = _database( tmp_path )
   _insert_enclosure( database, WOMBAT, AUSTRALASIA )
   _insert_schedule(
      database,
      WOMBAT,
      AUSTRALASIA,
      '2026-11-01',
      HORIZON.isoformat(),
      '9:00 AM',
      '11:00 AM',
      KEPT,
   )
   pages = {
      WebsitePage.url( '' ): '<html></html>',
      WebsitePage.url( AnimalCatalogue.PAGE ): QUIET_ANIMALS,
      WebsitePage.url( 'wombat' ): WOMBAT_PAGE,
   }
   monkeypatch.setattr(
      WebsitePage,
      'fetch_text',
      lambda url: _fetch( pages, url ),
   )
   before = CheckReport.fixed_count

   result = ViewingHoursChecker.check_schedules( database, TODAY )

   output = capsys.readouterr().out
   assert result == 0
   assert CheckReport.fixed_count == before
   assert CheckReport.category_line( 'checks.websiteOnly', 0 ) in output
   assert WOMBAT not in output

   connection = sqlite3.connect( database )
   message = connection.execute(
      'SELECT VIEWING_MESSAGE FROM AnimalVisibilitySchedule WHERE SPECIES = ?;',
      ( WOMBAT, ),
   ).fetchone()[ 0 ]
   connection.close()
   assert message == KEPT
