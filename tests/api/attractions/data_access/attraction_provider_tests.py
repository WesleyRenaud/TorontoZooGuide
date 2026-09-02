from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.attractions.data_access.attraction_provider import AttractionProvider


ATTRACTION_PROVIDER_SCHEMA = """
CREATE TABLE Attraction (
   NAME                     TEXT    NOT NULL PRIMARY KEY,
   FREE_WITH_ADMISSION      INTEGER NOT NULL,
   DESCRIPTION              TEXT    NOT NULL,
   INFO_LINK                TEXT    NOT NULL,
   HYPERLINK_TEXT           TEXT    NOT NULL,
   X_COORD                  REAL    NOT NULL,
   Y_COORD                  REAL    NOT NULL,
   REGION                   TEXT    NOT NULL,
   IS_ALSO_TRANSPORTATION   INTEGER NOT NULL
);

CREATE TABLE AttractionDaySeasonalAvailabilityMultiplier (
   ATTRACTION              TEXT    NOT NULL,
   MONTH                   INTEGER NOT NULL,
   DAY                     INTEGER NOT NULL,
   WEEKDAY_VALUE           REAL    NOT NULL,
   WEEKEND_HOLIDAY_VALUE   REAL    NOT NULL,
   PRIMARY KEY ( ATTRACTION, MONTH, DAY )
);

CREATE TABLE AttractionHoursSchedule (
   ATTRACTION                      TEXT NOT NULL,
   SCHEDULE_START_DATE             TEXT NOT NULL,
   SCHEDULE_END_DATE               TEXT,
   WEEKDAY_START_TIME              TEXT NOT NULL,
   WEEKDAY_END_TIME                TEXT NOT NULL,
   WEEKEND_HOLIDAY_START_TIME      TEXT NOT NULL,
   WEEKEND_HOLIDAY_END_TIME        TEXT NOT NULL,
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);

CREATE TABLE AttractionOpeningSchedule (
   ATTRACTION            TEXT    NOT NULL,
   SCHEDULE_START_DATE   TEXT    NOT NULL,
   SCHEDULE_END_DATE     TEXT,
   MONDAY                INTEGER NOT NULL DEFAULT 0,
   TUESDAY               INTEGER NOT NULL DEFAULT 0,
   WEDNESDAY             INTEGER NOT NULL DEFAULT 0,
   THURSDAY              INTEGER NOT NULL DEFAULT 0,
   FRIDAY                INTEGER NOT NULL DEFAULT 0,
   SATURDAY              INTEGER NOT NULL DEFAULT 0,
   SUNDAY                INTEGER NOT NULL DEFAULT 0,
   HOLIDAYS_ONLY         INTEGER NOT NULL DEFAULT 0,
   SCHEDULE_MESSAGE      TEXT,
   PRIMARY KEY ( ATTRACTION, SCHEDULE_START_DATE )
);

CREATE TABLE AttractionScheduleOverride (
   ATTRACTION            TEXT    NOT NULL,
   OVERRIDE_START_DATE   TEXT    NOT NULL,
   OVERRIDE_END_DATE     TEXT,
   IS_CLOSED             INTEGER NOT NULL DEFAULT 1,
   OVERRIDE_MESSAGE      TEXT,
   PRIMARY KEY ( ATTRACTION, OVERRIDE_START_DATE )
);
"""

CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'
VISIT_DATE = date( 2026, 6, 15 )
OTHER_DAY = date( 2026, 12, 25 )


@pytest.fixture
def attraction_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ATTRACTION_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _insert_attraction(
      conn: sqlite3.Connection,
      *,
      name: str,
      free_with_admission: int = 1,
      is_also_transportation: int = 0 ) -> None:
   conn.execute(
      """   INSERT INTO Attraction (
               NAME,
               FREE_WITH_ADMISSION,
               DESCRIPTION,
               INFO_LINK,
               HYPERLINK_TEXT,
               X_COORD,
               Y_COORD,
               REGION,
               IS_ALSO_TRANSPORTATION
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         name,
         free_with_admission,
         f'{ name } description',
         f'https://example.test/{ name }',
         'Learn more',
         10.5,
         20.5,
         'Tundra Trek',
         is_also_transportation,
      ),
   )


def Test_FetchAttractionNames_TestEmpty_ExpectEmptyList(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   assert AttractionProvider.fetch_attraction_names( attraction_provider_conn ) == []


def Test_FetchAttractionNames_TestPopulated_ExpectNames(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   _insert_attraction( attraction_provider_conn, name=CAROUSEL )
   _insert_attraction(
      attraction_provider_conn,
      name=ZOOMOBILE,
      free_with_admission=0,
      is_also_transportation=1 )
   attraction_provider_conn.commit()

   names = AttractionProvider.fetch_attraction_names( attraction_provider_conn )

   assert set( names ) == { CAROUSEL, ZOOMOBILE }


def Test_FetchAttractionRecords_TestNoMultiplierOrHours_ExpectDefaultMultipliersAndNullHours(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   _insert_attraction( attraction_provider_conn, name=CAROUSEL )
   attraction_provider_conn.commit()

   records = AttractionProvider.fetch_attraction_records(
      attraction_provider_conn,
      VISIT_DATE )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.name == CAROUSEL
   assert record.free_with_admission == 1
   assert record.description == f'{ CAROUSEL } description'
   assert record.info_link == f'https://example.test/{ CAROUSEL }'
   assert record.hyperlink_text == 'Learn more'
   assert record.x_coord == 10.5
   assert record.y_coord == 20.5
   assert record.region == 'Tundra Trek'
   assert record.weekday_multiplier == 1.0
   assert record.weekend_holiday_multiplier == 1.0
   assert record.weekday_start_time is None
   assert record.weekday_end_time is None
   assert record.weekend_holiday_start_time is None
   assert record.weekend_holiday_end_time is None
   assert record.is_also_transportation is False


def Test_FetchAttractionRecords_TestMatchingMultiplierAndHours_ExpectJoinedValues(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   _insert_attraction(
      attraction_provider_conn,
      name=ZOOMOBILE,
      free_with_admission=0,
      is_also_transportation=1 )
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionDaySeasonalAvailabilityMultiplier (
               ATTRACTION, MONTH, DAY, WEEKDAY_VALUE, WEEKEND_HOLIDAY_VALUE
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, 6, 15, 0.5, 0.75 ),
   )
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionHoursSchedule (
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               WEEKDAY_START_TIME,
               WEEKDAY_END_TIME,
               WEEKEND_HOLIDAY_START_TIME,
               WEEKEND_HOLIDAY_END_TIME
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         ZOOMOBILE,
         '2026-06-01',
         '2026-08-31',
         '10:00',
         '16:00',
         '09:30',
         '17:00',
      ),
   )
   attraction_provider_conn.commit()

   records = AttractionProvider.fetch_attraction_records(
      attraction_provider_conn,
      VISIT_DATE )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.name == ZOOMOBILE
   assert record.free_with_admission == 0
   assert record.weekday_multiplier == 0.5
   assert record.weekend_holiday_multiplier == 0.75
   assert record.weekday_start_time == '10:00'
   assert record.weekday_end_time == '16:00'
   assert record.weekend_holiday_start_time == '09:30'
   assert record.weekend_holiday_end_time == '17:00'
   assert record.is_also_transportation is True


def Test_FetchAttractionRecords_TestHoursOutsideVisitDate_ExpectNullHours(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   _insert_attraction( attraction_provider_conn, name=CAROUSEL )
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionHoursSchedule (
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               WEEKDAY_START_TIME,
               WEEKDAY_END_TIME,
               WEEKEND_HOLIDAY_START_TIME,
               WEEKEND_HOLIDAY_END_TIME
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         CAROUSEL,
         '2026-01-01',
         '2026-03-31',
         '10:00',
         '15:00',
         '10:00',
         '16:00',
      ),
   )
   attraction_provider_conn.commit()

   records = AttractionProvider.fetch_attraction_records(
      attraction_provider_conn,
      VISIT_DATE )

   assert len( records ) == 1
   assert records[ 0 ].weekday_start_time is None
   assert records[ 0 ].weekday_end_time is None


def Test_FetchAttractionRecordForCalendarDay_TestMissingAttraction_ExpectNone(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   assert AttractionProvider.fetch_attraction_record_for_calendar_day(
      attraction_provider_conn,
      CAROUSEL,
      VISIT_DATE ) is None


def Test_FetchAttractionRecordForCalendarDay_TestOpenEndedHours_ExpectJoinedHours(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   _insert_attraction( attraction_provider_conn, name=CAROUSEL )
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionHoursSchedule (
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               WEEKDAY_START_TIME,
               WEEKDAY_END_TIME,
               WEEKEND_HOLIDAY_START_TIME,
               WEEKEND_HOLIDAY_END_TIME
            )
            VALUES ( ?, ?, NULL, ?, ?, ?, ? );
      """,
      ( CAROUSEL, '2026-06-01', '11:00', '17:00', '10:00', '18:00' ),
   )
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionDaySeasonalAvailabilityMultiplier (
               ATTRACTION, MONTH, DAY, WEEKDAY_VALUE, WEEKEND_HOLIDAY_VALUE
            )
            VALUES ( ?, ?, ?, ?, ? );
      """,
      ( CAROUSEL, 12, 25, 0.2, 0.3 ),
   )
   attraction_provider_conn.commit()

   matching = AttractionProvider.fetch_attraction_record_for_calendar_day(
      attraction_provider_conn,
      CAROUSEL,
      VISIT_DATE )
   other_day = AttractionProvider.fetch_attraction_record_for_calendar_day(
      attraction_provider_conn,
      CAROUSEL,
      OTHER_DAY )

   assert matching is not None
   assert matching.weekday_start_time == '11:00'
   assert matching.weekday_multiplier == 1.0
   assert other_day is not None
   assert other_day.weekday_multiplier == 0.2
   assert other_day.weekend_holiday_multiplier == 0.3
   assert other_day.weekday_start_time == '11:00'


def Test_FetchAttractionScheduleRecords_TestEmpty_ExpectEmptyList(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   assert AttractionProvider.fetch_attraction_schedule_records(
      attraction_provider_conn ) == []


def Test_FetchAttractionScheduleRecords_TestPopulated_ExpectMappedFields(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionOpeningSchedule (
               ATTRACTION,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               HOLIDAYS_ONLY,
               SCHEDULE_MESSAGE
            )
            VALUES ( ?, ?, ?, 1, 1, 1, 1, 1, 0, 0, 0, ? );
      """,
      ( CAROUSEL, '2026-05-01', '2026-09-30', 'Weekdays only' ),
   )
   attraction_provider_conn.commit()

   records = AttractionProvider.fetch_attraction_schedule_records(
      attraction_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.attraction == CAROUSEL
   assert record.schedule_start_date == '2026-05-01'
   assert record.schedule_end_date == '2026-09-30'
   assert record.monday == 1
   assert record.saturday == 0
   assert record.holidays_only == 0
   assert record.schedule_message == 'Weekdays only'


def Test_FetchAttractionScheduleOverrideRecords_TestEmpty_ExpectEmptyList(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   assert AttractionProvider.fetch_attraction_schedule_override_records(
      attraction_provider_conn ) == []


def Test_FetchAttractionScheduleOverrideRecords_TestPopulated_ExpectMappedFields(
      attraction_provider_conn: sqlite3.Connection ) -> None:
   attraction_provider_conn.execute(
      """   INSERT INTO AttractionScheduleOverride (
               ATTRACTION,
               OVERRIDE_START_DATE,
               OVERRIDE_END_DATE,
               IS_CLOSED,
               OVERRIDE_MESSAGE
            )
            VALUES ( ?, ?, ?, 1, ? );
      """,
      ( CAROUSEL, '2026-07-01', '2026-07-07', 'Closed for maintenance' ),
   )
   attraction_provider_conn.commit()

   records = AttractionProvider.fetch_attraction_schedule_override_records(
      attraction_provider_conn )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.attraction == CAROUSEL
   assert record.override_start_date == '2026-07-01'
   assert record.override_end_date == '2026-07-07'
   assert record.is_closed == 1
   assert record.override_message == 'Closed for maintenance'
