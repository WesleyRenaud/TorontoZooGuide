from __future__ import annotations

import sqlite3

import pytest

from api.animals.data_access.animal_viewable_on_day_provider import AnimalViewableOnDayProvider


SPECIES = 'Amur Tiger'
OTHER_SPECIES = 'Snow Leopard'
EXHIBIT = 'Eurasia Wilds'
OTHER_EXHIBIT = 'Canadian Domain'
VISIT_MONTH = 6
VISIT_DAY = 15

ANIMAL_VIEWABLE_ON_DAY_PROVIDER_SCHEMA = """
CREATE TABLE Animal (
   SPECIES                     TEXT NOT NULL PRIMARY KEY,
   LATIN_NAME                  TEXT,
   MIN_TEMPERATURE             INTEGER,
   GENERAL_VIEWING_TIPS        TEXT,
   SEASONAL_VIEWING_TIPS       TEXT,
   IDENTIFICATION              TEXT,
   HABITAT_AND_RANGE           TEXT,
   DIET_AND_FEEDING            TEXT,
   BEHAVIOUR_AND_SOCIAL_LIFE   TEXT,
   ADAPTATIONS                 TEXT,
   REPRODUCTION_AND_LIFE_CYCLE TEXT,
   ANIMALS_AT_THE_ZOO          TEXT
);

CREATE TABLE Enclosure (
   SPECIES                       TEXT NOT NULL,
   EXHIBIT                       TEXT NOT NULL,
   SEASONAL_VIEWING_SUMMARY      TEXT NOT NULL,
   SEASONAL_VIEWING_INFORMATION  TEXT,
   INCLUDE_ALL_VIEWING_SPOTS     INTEGER,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);

CREATE TABLE EnclosureViewing (
   SPECIES                        TEXT NOT NULL,
   EXHIBIT                        TEXT NOT NULL,
   NAME                           TEXT,
   ENCLOSURE_TYPE                 TEXT NOT NULL,
   SEASONALLY_OFF_DISPLAY_MESSAGE TEXT,
   X_COORD                        REAL NOT NULL,
   Y_COORD                        REAL NOT NULL,
   IS_ZOOMOBILE_ONLY              INTEGER NOT NULL DEFAULT 0,
   PRIMARY KEY ( SPECIES, EXHIBIT, NAME )
);

CREATE TABLE AnimalStatus (
   SPECIES              TEXT NOT NULL,
   EXHIBIT              TEXT NOT NULL,
   VIEWING_SCOPE        TEXT NOT NULL,
   IS_OFF_DISPLAY       INTEGER NOT NULL,
   OFF_DISPLAY_MESSAGE  TEXT,
   OFF_DISPLAY_START    TEXT,
   OFF_DISPLAY_END      TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT, VIEWING_SCOPE )
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

CREATE TABLE AnimalViewingAlert (
   SPECIES           TEXT NOT NULL,
   EXHIBIT           TEXT NOT NULL,
   ALERT_MESSAGE     TEXT NOT NULL,
   ALERT_START_DATE  TEXT,
   ALERT_END_DATE    TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT )
);

CREATE TABLE ExhibitStatus (
   EXHIBIT         TEXT NOT NULL PRIMARY KEY,
   IS_CLOSED       INTEGER NOT NULL,
   CLOSED_MESSAGE  TEXT,
   CLOSED_START    TEXT,
   CLOSED_END      TEXT
);

CREATE TABLE AnimalDaySeasonalViewabilityMultiplier (
   SPECIES  TEXT NOT NULL,
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    REAL NOT NULL,
   PRIMARY KEY ( SPECIES, EXHIBIT, MONTH, DAY )
);

CREATE TABLE ExhibitDaySeasonalAvailabilityMultiplier (
   EXHIBIT  TEXT NOT NULL,
   MONTH    INTEGER NOT NULL,
   DAY      INTEGER NOT NULL,
   VALUE    REAL NOT NULL,
   PRIMARY KEY ( EXHIBIT, MONTH, DAY )
);
"""


@pytest.fixture
def animal_viewable_on_day_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( ANIMAL_VIEWABLE_ON_DAY_PROVIDER_SCHEMA )

   yield conn

   conn.close()


def _seed_base_animal(
      conn: sqlite3.Connection,
      *,
      species: str = SPECIES,
      exhibit: str = EXHIBIT,
      enclosure_name: str = 'Outdoor Yard',
      enclosure_type: str = 'Outdoor' ) -> None:
   conn.execute(
      """   INSERT OR IGNORE INTO Animal (
               SPECIES,
               LATIN_NAME,
               MIN_TEMPERATURE,
               GENERAL_VIEWING_TIPS,
               SEASONAL_VIEWING_TIPS,
               IDENTIFICATION,
               HABITAT_AND_RANGE,
               DIET_AND_FEEDING,
               BEHAVIOUR_AND_SOCIAL_LIFE,
               ADAPTATIONS,
               REPRODUCTION_AND_LIFE_CYCLE,
               ANIMALS_AT_THE_ZOO
            ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         f'{ species } latin',
         -10,
         'tips',
         'seasonal tips',
         'id',
         'habitat',
         'diet',
         'behaviour',
         'adaptations',
         'reproduction',
         'at zoo',
      ),
   )
   conn.execute(
      """   INSERT OR IGNORE INTO Enclosure (
               SPECIES,
               EXHIBIT,
               SEASONAL_VIEWING_SUMMARY,
               SEASONAL_VIEWING_INFORMATION,
               INCLUDE_ALL_VIEWING_SPOTS
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      ( species, exhibit, 'summary', 'information', 1 ),
   )
   conn.execute(
      """   INSERT INTO EnclosureViewing (
               SPECIES,
               EXHIBIT,
               NAME,
               ENCLOSURE_TYPE,
               SEASONALLY_OFF_DISPLAY_MESSAGE,
               X_COORD,
               Y_COORD,
               IS_ZOOMOBILE_ONLY
            ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         enclosure_name,
         enclosure_type,
         None,
         1.0,
         2.0,
         0,
      ),
   )


def Test_FetchAnimalsViewableOnDayRecords_TestEmpty_ExpectEmptyList(
      animal_viewable_on_day_conn: sqlite3.Connection ) -> None:
   assert AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY ) == []


def Test_FetchAnimalsViewableOnDayRecords_TestDefaults_ExpectDefaultMultipliers(
      animal_viewable_on_day_conn: sqlite3.Connection ) -> None:
   _seed_base_animal( animal_viewable_on_day_conn )
   animal_viewable_on_day_conn.commit()

   records = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.species == SPECIES
   assert record.exhibit == EXHIBIT
   assert record.enclosure_name == 'Outdoor Yard'
   assert record.enclosure_type == 'Outdoor'
   assert record.latin_name == f'{ SPECIES } latin'
   assert record.min_temperature == -10
   assert record.include_all_viewing_spots is True
   assert record.is_zoomobile_only is False
   assert record.is_off_display is None
   assert record.viewing_scope is None
   assert record.schedule_start_date is None
   assert record.alert_message is None
   assert record.is_closed is None
   assert record.animal_day_seasonal_multiplier == 1.0
   assert record.exhibit_day_seasonal_availability_multiplier == 1.0


def Test_FetchAnimalsViewableOnDayRecords_TestJoinedStatusScheduleAlertAndMultipliers_ExpectMapped(
      animal_viewable_on_day_conn: sqlite3.Connection ) -> None:
   _seed_base_animal( animal_viewable_on_day_conn )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, VIEWING_SCOPE, IS_OFF_DISPLAY,
               OFF_DISPLAY_MESSAGE, OFF_DISPLAY_START, OFF_DISPLAY_END
            ) VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      ( SPECIES, EXHIBIT, 'all', 1, 'Off display.', '2026-06-01', '2026-06-30' ),
   )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO AnimalVisibilitySchedule (
               SPECIES, EXHIBIT, SCHEDULE_START_DATE, SCHEDULE_END_DATE,
               DAILY_START_TIME, DAILY_END_TIME, VIEWING_MESSAGE
            ) VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      ( SPECIES, EXHIBIT, '2026-06-01', '2026-06-30', '09:00', '11:00', 'Morning only.' ),
   )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO AnimalViewingAlert (
               SPECIES, EXHIBIT, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      ( SPECIES, EXHIBIT, 'Construction nearby.', '2026-06-10', '2026-06-20' ),
   )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO ExhibitStatus (
               EXHIBIT, IS_CLOSED, CLOSED_MESSAGE, CLOSED_START, CLOSED_END
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      ( EXHIBIT, 1, 'Closed for maintenance.', '2026-06-01', '2026-06-05' ),
   )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO AnimalDaySeasonalViewabilityMultiplier (
               SPECIES, EXHIBIT, MONTH, DAY, VALUE
            ) VALUES ( ?, ?, ?, ?, ? );
      """,
      ( SPECIES, EXHIBIT, VISIT_MONTH, VISIT_DAY, 0.4 ),
   )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO ExhibitDaySeasonalAvailabilityMultiplier (
               EXHIBIT, MONTH, DAY, VALUE
            ) VALUES ( ?, ?, ?, ? );
      """,
      ( EXHIBIT, VISIT_MONTH, VISIT_DAY, 0.7 ),
   )
   animal_viewable_on_day_conn.commit()

   records = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   record = records[ 0 ]
   assert record.is_off_display == 1
   assert record.viewing_scope.value == 'all'
   assert record.off_display_message == 'Off display.'
   assert record.off_display_start == '2026-06-01'
   assert record.off_display_end == '2026-06-30'
   assert record.schedule_start_date == '2026-06-01'
   assert record.schedule_end_date == '2026-06-30'
   assert record.daily_start_time == '09:00'
   assert record.daily_end_time == '11:00'
   assert record.viewing_message == 'Morning only.'
   assert record.alert_message == 'Construction nearby.'
   assert record.alert_start_date == '2026-06-10'
   assert record.alert_end_date == '2026-06-20'
   assert record.is_closed == 1
   assert record.closed_message == 'Closed for maintenance.'
   assert record.closed_start == '2026-06-01'
   assert record.closed_end == '2026-06-05'
   assert record.animal_day_seasonal_multiplier == 0.4
   assert record.exhibit_day_seasonal_availability_multiplier == 0.7


def Test_FetchAnimalsViewableOnDayRecords_TestExhibitFilter_ExpectOnlyMatchingExhibits(
      animal_viewable_on_day_conn: sqlite3.Connection ) -> None:
   _seed_base_animal( animal_viewable_on_day_conn )
   _seed_base_animal(
      animal_viewable_on_day_conn,
      species=OTHER_SPECIES,
      exhibit=OTHER_EXHIBIT,
      enclosure_name='Forest Yard' )
   animal_viewable_on_day_conn.commit()

   records = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY,
      exhibits_to_include=[ EXHIBIT, '  ', '', OTHER_EXHIBIT ] )

   assert { record.exhibit for record in records } == { EXHIBIT, OTHER_EXHIBIT }

   filtered = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY,
      exhibits_to_include=[ OTHER_EXHIBIT ] )

   assert len( filtered ) == 1
   assert filtered[ 0 ].species == OTHER_SPECIES
   assert filtered[ 0 ].exhibit == OTHER_EXHIBIT


def Test_FetchAnimalsViewableOnDayRecords_TestWhitespaceOnlyExhibits_ExpectUnfiltered(
      animal_viewable_on_day_conn: sqlite3.Connection ) -> None:
   _seed_base_animal( animal_viewable_on_day_conn )
   _seed_base_animal(
      animal_viewable_on_day_conn,
      species=OTHER_SPECIES,
      exhibit=OTHER_EXHIBIT,
      enclosure_name='Forest Yard' )
   animal_viewable_on_day_conn.commit()

   records = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY,
      exhibits_to_include=[ '  ', '' ] )

   assert { record.exhibit for record in records } == { EXHIBIT, OTHER_EXHIBIT }


def Test_FetchAnimalsViewableOnDayRecords_TestScopeMatchingEnclosureType_ExpectJoinedStatus(
      animal_viewable_on_day_conn: sqlite3.Connection ) -> None:
   _seed_base_animal(
      animal_viewable_on_day_conn,
      enclosure_type='Outdoor' )
   animal_viewable_on_day_conn.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, VIEWING_SCOPE, IS_OFF_DISPLAY,
               OFF_DISPLAY_MESSAGE, OFF_DISPLAY_START, OFF_DISPLAY_END
            ) VALUES ( ?, ?, ?, ?, ?, ?, ? );
      """,
      ( SPECIES, EXHIBIT, 'Outdoor', 1, 'Outdoor closed.', '2026-06-01', '2026-06-30' ),
   )
   animal_viewable_on_day_conn.commit()

   records = AnimalViewableOnDayProvider.fetch_animals_viewable_on_day_records(
      animal_viewable_on_day_conn,
      VISIT_MONTH,
      VISIT_DAY )

   assert len( records ) == 1
   assert records[ 0 ].is_off_display == 1
   assert records[ 0 ].off_display_message == 'Outdoor closed.'
   assert records[ 0 ].viewing_scope.value == 'outdoor'
