from __future__ import annotations

import sqlite3

import pytest

from api.zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider


ZOO_HOURS_PROVIDER_SCHEMA = """
CREATE TABLE ZooHours (
   OPERATING_DATE       TEXT        NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME TEXT,
   OPEN_TIME            TEXT        NOT NULL,
   LAST_ADMISSION_TIME  TEXT        NOT NULL,
   CLOSE_TIME           TEXT        NOT NULL
);
"""

JUNE_20_ROW = (
   '2026-06-20',
   '09:00',
   '09:30',
   '18:00',
   '19:00',
)
JUNE_22_ROW = (
   '2026-06-22',
   None,
   '09:30',
   '17:00',
   '18:00',
)
DECEMBER_25_ROW = (
   '2026-12-25',
   None,
   '11:00',
   '15:00',
   '16:00',
)


@pytest.fixture
def zoo_hours_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ZOO_HOURS_PROVIDER_SCHEMA )
   conn.executemany(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      [
         JUNE_20_ROW,
         JUNE_22_ROW,
         DECEMBER_25_ROW,
      ],
   )
   conn.commit()

   yield conn

   conn.close()


def Test_FetchZooHoursRecord_TestJune20_ExpectEarlyAdmissionHours(
      zoo_hours_provider_conn: sqlite3.Connection ) -> None:
   record = ZooHoursProvider.fetch_zoo_hours_record(
      zoo_hours_provider_conn,
      '2026-06-20' )

   assert record is not None
   assert record.operating_date == '2026-06-20'
   assert record.early_admission_time == '09:00'
   assert record.open_time == '09:30'
   assert record.last_admission_time == '18:00'
   assert record.close_time == '19:00'


def Test_FetchZooHoursRecord_TestJune22_ExpectStandardHours(
      zoo_hours_provider_conn: sqlite3.Connection ) -> None:
   record = ZooHoursProvider.fetch_zoo_hours_record(
      zoo_hours_provider_conn,
      '2026-06-22' )

   assert record is not None
   assert record.early_admission_time is None
   assert record.open_time == '09:30'
   assert record.last_admission_time == '17:00'
   assert record.close_time == '18:00'


def Test_FetchZooHoursRecord_TestDecember25_ExpectHolidayHours(
      zoo_hours_provider_conn: sqlite3.Connection ) -> None:
   record = ZooHoursProvider.fetch_zoo_hours_record(
      zoo_hours_provider_conn,
      '2026-12-25' )

   assert record is not None
   assert record.early_admission_time is None
   assert record.open_time == '11:00'
   assert record.last_admission_time == '15:00'
   assert record.close_time == '16:00'
