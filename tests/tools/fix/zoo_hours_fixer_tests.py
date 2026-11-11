from __future__ import annotations

from pathlib import Path
import sqlite3

from api.models import ZooHours
from api.zoo_hours.data_access.zoo_hours_record import ZooHoursRecord
from tools.checks.check_report import CheckReport
from tools.fix.zoo_hours_fixer import ZooHoursFixer


SCHEMA = """
CREATE TABLE ZooHours (
   OPERATING_DATE DATE NOT NULL PRIMARY KEY,
   EARLY_ADMISSION_TIME TEXT,
   OPEN_TIME TEXT NOT NULL,
   LAST_ADMISSION_TIME TEXT NOT NULL,
   CLOSE_TIME TEXT NOT NULL
);
"""
WINTER = ZooHours(
   date='2026-11-03',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='15:30',
   close_time='16:30',
)
EARLY = ZooHours(
   date='2026-11-03',
   early_admission_time='09:00',
   open_time='09:30',
   last_admission_time='15:30',
   close_time='16:30',
)
EXTRA = ZooHours(
   date='2026-11-04',
   early_admission_time=None,
   open_time='09:30',
   last_admission_time='17:00',
   close_time='18:00',
)



def _write_database( path: Path, hours: list[ ZooHours ] ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.executemany(
      """   INSERT INTO ZooHours (
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            ) VALUES ( ?, ?, ?, ?, ? )
      """,
      [
         (
            item.date,
            item.early_admission_time,
            item.open_time,
            item.last_admission_time,
            item.close_time,
         )
         for item in hours
      ],
   )
   connection.commit()
   connection.close()


def _stored( path: Path ) -> list[ ZooHoursRecord ]:
   connection = sqlite3.connect( path )
   rows = connection.execute(
      """   SELECT
               OPERATING_DATE,
               EARLY_ADMISSION_TIME,
               OPEN_TIME,
               LAST_ADMISSION_TIME,
               CLOSE_TIME
            FROM ZooHours
            ORDER BY OPERATING_DATE
      """
   ).fetchall()
   connection.close()
   return [
      ZooHoursRecord(
         operating_date=row[ 0 ],
         early_admission_time=row[ 1 ],
         open_time=row[ 2 ],
         last_admission_time=row[ 3 ],
         close_time=row[ 4 ],
      )
      for row in rows
   ]


def _record( hours: ZooHours ) -> ZooHoursRecord:
   return ZooHoursRecord(
      operating_date=hours.date,
      early_admission_time=hours.early_admission_time,
      open_time=hours.open_time,
      last_admission_time=hours.last_admission_time,
      close_time=hours.close_time,
   )


def Test_Apply_TestNothingToChange_ExpectDatabaseUnchanged( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ WINTER ] )
   CheckReport.reset_fixed_count()

   ZooHoursFixer.apply( database, [], [] )

   assert _stored( database ) == [ _record( WINTER ) ]
   assert CheckReport.fixed_count == 0


def Test_Apply_TestMissingDay_ExpectSaved( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [] )
   CheckReport.reset_fixed_count()

   ZooHoursFixer.apply( database, [ WINTER ], [] )

   assert _stored( database ) == [ _record( WINTER ) ]
   assert CheckReport.fixed_count == 1


def Test_Apply_TestDifferentClocks_ExpectUpdated( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ EARLY ] )
   CheckReport.reset_fixed_count()

   ZooHoursFixer.apply( database, [ WINTER ], [] )

   assert _stored( database ) == [ _record( WINTER ) ]
   assert CheckReport.fixed_count == 1


def Test_Apply_TestAppOnlyDay_ExpectRemoved( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ WINTER, EXTRA ] )
   CheckReport.reset_fixed_count()

   ZooHoursFixer.apply( database, [], [ EXTRA ] )

   assert _stored( database ) == [ _record( WINTER ) ]
   assert CheckReport.fixed_count == 1


def Test_Apply_TestSaveAndRemove_ExpectBoth( tmp_path: Path ) -> None:
   database = tmp_path / 'animals.db'
   _write_database( database, [ EXTRA ] )
   CheckReport.reset_fixed_count()

   ZooHoursFixer.apply( database, [ WINTER ], [ EXTRA ] )

   assert _stored( database ) == [ _record( WINTER ) ]
   assert CheckReport.fixed_count == 2
