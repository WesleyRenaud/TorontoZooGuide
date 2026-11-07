from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.enclosure_off_display_month_provider import EnclosureOffDisplayMonthProvider
from api.animals.domain.enclosure_off_display_month import EnclosureOffDisplayMonth


ENCLOSURE_SCHEMA = """
CREATE TABLE Enclosure (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH INTEGER
);
"""


@pytest.fixture
def enclosure_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ENCLOSURE_SCHEMA )

   yield conn

   conn.close()


def Test_FetchOffDisplayMonths_TestRows_ExpectSpeciesExhibitAndMonth(
      enclosure_conn: sqlite3.Connection ) -> None:
   enclosure_conn.executemany(
      """   INSERT INTO Enclosure (
               SPECIES,
               EXHIBIT,
               OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH
            )
            VALUES ( ?, ?, ? );
      """,
      [
         ( 'Warthog', 'Africa Savanna', 4 ),
         ( 'African Lion', 'Africa Savanna', None ),
      ],
   )
   enclosure_conn.commit()

   months = EnclosureOffDisplayMonthProvider.fetch_off_display_months( enclosure_conn )

   assert months == [
      EnclosureOffDisplayMonth(
         species='African Lion',
         exhibit='Africa Savanna',
         until_month=None ),
      EnclosureOffDisplayMonth(
         species='Warthog',
         exhibit='Africa Savanna',
         until_month=4 ),
   ]


def Test_FetchUntilMonth_TestApril_ExpectMonth(
      enclosure_conn: sqlite3.Connection ) -> None:
   enclosure_conn.execute(
      """   INSERT INTO Enclosure (
               SPECIES,
               EXHIBIT,
               OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH
            )
            VALUES ( ?, ?, ? );
      """,
      ( 'Warthog', 'Africa Savanna', 4 ),
   )
   enclosure_conn.commit()

   month = EnclosureOffDisplayMonthProvider.fetch_until_month(
      enclosure_conn,
      species='Warthog',
      exhibit='Africa Savanna' )

   assert month == 4


def Test_FetchUntilMonth_TestNullMonth_ExpectNone(
      enclosure_conn: sqlite3.Connection ) -> None:
   enclosure_conn.execute(
      """   INSERT INTO Enclosure (
               SPECIES,
               EXHIBIT,
               OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH
            )
            VALUES ( ?, ?, ? );
      """,
      ( 'African Lion', 'Africa Savanna', None ),
   )
   enclosure_conn.commit()

   month = EnclosureOffDisplayMonthProvider.fetch_until_month(
      enclosure_conn,
      species='African Lion',
      exhibit='Africa Savanna' )

   assert month == None


def Test_FetchUntilMonth_TestMissingEnclosure_ExpectRaises(
      enclosure_conn: sqlite3.Connection ) -> None:
   with pytest.raises( TypeError ):
      EnclosureOffDisplayMonthProvider.fetch_until_month(
         enclosure_conn,
         species='Warthog',
         exhibit='Africa Savanna' )
