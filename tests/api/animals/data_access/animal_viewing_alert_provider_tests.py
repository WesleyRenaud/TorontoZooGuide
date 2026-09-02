from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_viewing_alert_provider import AnimalViewingAlertProvider


SPECIES = 'Amur Tiger'
EXHIBIT = 'Eurasia Wilds'
ALERT_START_DATE = '2026-06-01'
ALERT_END_DATE = '2026-06-30'
MESSAGE = 'May be difficult to spot.'

ANIMAL_VIEWING_ALERT_SCHEMA = """
CREATE TABLE AnimalViewingAlert (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   ALERT_MESSAGE        TEXT,
   ALERT_START_DATE     TEXT,
   ALERT_END_DATE       TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);
"""


@pytest.fixture
def animal_viewing_alert_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_VIEWING_ALERT_SCHEMA )

   yield conn

   conn.close()


def Test_SaveAnimalViewingAlert_TestNewAlert_ExpectPersistsRow(
      animal_viewing_alert_conn: sqlite3.Connection ) -> None:
   assert AnimalViewingAlertProvider.save_animal_viewing_alert(
      animal_viewing_alert_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=MESSAGE ) is True

   row = animal_viewing_alert_conn.execute(
      """   SELECT SPECIES, EXHIBIT, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            FROM AnimalViewingAlert
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
      """,
      ( SPECIES, EXHIBIT ) ).fetchone()

   assert tuple( row ) == (
      SPECIES,
      EXHIBIT,
      MESSAGE,
      ALERT_START_DATE,
      ALERT_END_DATE,
   )


def Test_SaveAnimalViewingAlert_TestExistingAlert_ExpectReplacesRow(
      animal_viewing_alert_conn: sqlite3.Connection ) -> None:
   AnimalViewingAlertProvider.save_animal_viewing_alert(
      animal_viewing_alert_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=MESSAGE )

   assert AnimalViewingAlertProvider.save_animal_viewing_alert(
      animal_viewing_alert_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      alert_start_date='2026-07-01',
      alert_end_date='2026-07-15',
      message='Updated alert.' ) is True

   rows = animal_viewing_alert_conn.execute(
      """   SELECT ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            FROM AnimalViewingAlert
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
      """,
      ( SPECIES, EXHIBIT ) ).fetchall()

   assert len( rows ) == 1
   assert tuple( rows[ 0 ] ) == ( 'Updated alert.', '2026-07-01', '2026-07-15' )


def Test_DeleteAnimalViewingAlert_TestExistingAlert_ExpectRemovesRow(
      animal_viewing_alert_conn: sqlite3.Connection ) -> None:
   AnimalViewingAlertProvider.save_animal_viewing_alert(
      animal_viewing_alert_conn,
      species=SPECIES,
      exhibit=EXHIBIT,
      alert_start_date=ALERT_START_DATE,
      alert_end_date=ALERT_END_DATE,
      message=MESSAGE )

   assert AnimalViewingAlertProvider.delete_animal_viewing_alert(
      animal_viewing_alert_conn,
      species=SPECIES,
      exhibit=EXHIBIT ) is True

   row = animal_viewing_alert_conn.execute(
      """   SELECT 1
            FROM AnimalViewingAlert
            WHERE SPECIES = ?
               AND EXHIBIT = ?;
      """,
      ( SPECIES, EXHIBIT ) ).fetchone()

   assert row is None


def Test_DeleteAnimalViewingAlert_TestMissingAlert_ExpectFalse(
      animal_viewing_alert_conn: sqlite3.Connection ) -> None:
   assert AnimalViewingAlertProvider.delete_animal_viewing_alert(
      animal_viewing_alert_conn,
      species=SPECIES,
      exhibit=EXHIBIT ) is False
