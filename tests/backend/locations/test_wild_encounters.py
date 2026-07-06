from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

def test_wild_encounter_schedule_and_cancellation(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None
   )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '2:00 PM' )
   assert encounter.is_available is True
   assert encounter.maximum_duration == 45
   assert encounter.end_time == '2:45 PM'

   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-15',
      encounter_times=[ '2:00 PM' ]
   )
   encounters_after_cancel = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   cancelled = next( item for item in encounters_after_cancel if item.name == 'African Rainforest' and item.start_time == '2:00 PM' )
   assert cancelled.is_available is False

   weekday_unavailable = next(
      item for item in WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=16, year=2026 )
      if item.name == 'African Rainforest' and item.start_time == '2:00 PM'
   )
   out_of_range = next(
      item for item in WildEncounterCoordinator.get_wild_encounter_schedule( month='July', day=1, year=2026 )
      if item.name == 'African Rainforest' and item.start_time == '2:00 PM'
   )
   assert weekday_unavailable.unavailable_message == 'African Rainforest is not offered on this day of the week.'
   assert out_of_range.unavailable_message == 'African Rainforest is not scheduled on July 1.'


def test_wild_encounter_search_only_returns_available_schedule_days(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Mischevious Meerkats',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row( '14:00', monday=True, tuesday=False, wednesday=True, thursday=True, friday=False, saturday=True, sunday=False ),
      ],
      message=None
   )

   monday_results = WildEncounterCoordinator.get_wild_encounters_matching_query(
      query='Mischevious Meerkats',
      month='June',
      day=15,
      year=2026 )
   sunday_results = WildEncounterCoordinator.get_wild_encounters_matching_query(
      query='Mischevious Meerkats',
      month='June',
      day=21,
      year=2026 )
   sunday_available = WildEncounterCoordinator.get_available_wild_encounters(
      month='June',
      day=21,
      year=2026 )

   assert [ item.name for item in monday_results ] == [ 'Mischevious Meerkats' ]
   assert sunday_results == []
   assert all( item.name != 'Mischevious Meerkats' for item in sunday_available )


def test_wild_encounter_occurrences_cover_all_weekdays_and_cancellations(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-15',
      end_date='2026-06-21',
      schedule_rows=[
         wire_schedule_row( '14:00', monday=True, tuesday=True, wednesday=True, thursday=True, friday=True, saturday=True, sunday=True ),
      ],
      message=None
   )
   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='African Rainforest',
      date='2026-06-18',
      encounter_times=[ '2:00 PM' ]
   )

   occurrences = WildEncounterCoordinator.get_wild_encounter_occurrences(
      wild_encounter_name='African Rainforest',
      days_ahead=6
   )

   assert { occurrence.date for occurrence in occurrences } == {
      '2026-06-15',
      '2026-06-16',
      '2026-06-17',
      '2026-06-19',
      '2026-06-20',
      '2026-06-21'
   }
   assert WildEncounterCoordinator.get_wild_encounter_occurrences( wild_encounter_name='' ) == []
   assert WildEncounterCoordinator.get_wild_encounter_occurrences( wild_encounter_name='Bad Encounter' ) == []


def test_wild_encounter_schedule_accepts_multiple_times_on_one_day(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00', '15:30' ),
      message=None
   )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   rainforest_times = sorted(
      item.start_time
      for item in encounters
      if item.name == 'African Rainforest' and item.is_available
   )

   assert rainforest_times == [ '2:00 PM', '3:30 PM' ]


def test_wild_encounter_schedule_deduplicates_equivalent_time_formats(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '3:30 PM', '15:30', '14:00' ),
      message=None
   )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   rainforest_times = sorted(
      item.start_time
      for item in encounters
      if item.name == 'African Rainforest' and item.is_available
   )

   assert rainforest_times == [ '2:00 PM', '3:30 PM' ]


def test_wild_encounter_schedule_rejects_overlapping_date_ranges_for_same_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   db.conn.execute(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY,
               ENCOUNTER_TIME,
               SCHEDULE_MESSAGE
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
      (
         'African Rainforest',
         '2026-05-01',
         '2026-06-30',
         1,
         0,
         0,
         0,
         0,
         0,
         0,
         '3:30 PM',
         'Old schedule.',
      ) )
   db.conn.commit()

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '15:30' ),
      message='Updated schedule.'
   ) is False

   assert WildEncounterCoordinator.replace_wild_encounter_schedule_overlaps(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '15:30' ),
      message='Updated schedule.'
   )

   stored_times = [
      row[ 0 ]
      for row in db.conn.execute(
         """   SELECT ENCOUNTER_TIME
               FROM WildEncounterSchedule
               WHERE WILD_ENCOUNTER = 'African Rainforest';"""
      ).fetchall()
   ]

   assert stored_times == [ '3:30 PM' ]

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   rainforest = next(
      item for item in encounters
      if item.name == 'African Rainforest' and item.start_time == '3:30 PM'
   )

   assert rainforest.is_available is True


def test_wild_encounter_schedule_times_lists_distinct_scheduled_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '2:00 PM', '3:30 PM' ),
      message=None
   )

   assert WildEncounterCoordinator.get_wild_encounter_schedule_times(
      'African Rainforest' ) == [ '2:00 PM', '3:30 PM' ]


def test_wild_encounter_schedule_times_returns_stored_encounter_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   cur = db.conn.cursor()
   cur.execute(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               ENCOUNTER_TIME,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
      (
         'Savanna Safari',
         '2026-06-01',
         '2026-06-30',
         '2:00 PM',
         1,
         0,
         0,
         0,
         0,
         0,
         0,
      ) )
   cur.execute(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               ENCOUNTER_TIME,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
      (
         'Savanna Safari',
         '2026-06-01',
         '2026-06-30',
         '3:30 PM',
         1,
         0,
         0,
         0,
         0,
         0,
         0,
      ) )
   db.conn.commit()

   assert WildEncounterCoordinator.get_wild_encounter_schedule_times(
      'Savanna Safari' ) == [ '2:00 PM', '3:30 PM' ]


def test_wild_encounter_schedule_end_accepts_multiple_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '2:00 PM', '3:30 PM' ),
      message=None
   )

   assert WildEncounterCoordinator.end_wild_encounter_schedule(
      wild_encounter_name='African Rainforest',
      schedule_end_date='2026-06-14',
      encounter_times=[ '2:00 PM', '3:30 PM' ] )

   assert WildEncounterCoordinator.get_wild_encounter_schedule_times(
      'African Rainforest' ) == []

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   available_times = sorted(
      item.start_time
      for item in encounters
      if item.name == 'African Rainforest' and item.is_available
   )

   assert available_times == []

   unavailable_times = sorted(
      item.start_time
      for item in encounters
      if item.name == 'African Rainforest' and not item.is_available
   )

   assert unavailable_times == [ '2:00 PM', '3:30 PM' ]


def test_wild_encounter_schedule_times_excludes_ended_trimmed_rows(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 7, 6 ) )

   cur = db.conn.cursor()
   for encounter_time in ( '10:00 AM', '3:30 PM' ):
      cur.execute(
         """   INSERT INTO WildEncounterSchedule (
                  WILD_ENCOUNTER,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ENCOUNTER_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
         (
            'Kangaroo',
            '2026-06-28',
            '2026-07-05',
            encounter_time,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
         ) )
      cur.execute(
         """   INSERT INTO WildEncounterSchedule (
                  WILD_ENCOUNTER,
                  SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE,
                  ENCOUNTER_TIME,
                  MONDAY,
                  TUESDAY,
                  WEDNESDAY,
                  THURSDAY,
                  FRIDAY,
                  SATURDAY,
                  SUNDAY
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
         (
            'Kangaroo',
            '2026-07-06',
            None,
            encounter_time,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
         ) )
   db.conn.commit()

   assert WildEncounterCoordinator.get_wild_encounter_schedule_times(
      'Kangaroo' ) == [ '10:00 AM', '3:30 PM' ]

   assert WildEncounterCoordinator.end_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      schedule_end_date='2026-07-10',
      encounter_times=[ '10:00 AM', '3:30 PM' ] )

   cur.execute(
      """   SELECT
               SCHEDULE_START_DATE,
               SCHEDULE_END_DATE,
               ENCOUNTER_TIME
            FROM WildEncounterSchedule
            WHERE WILD_ENCOUNTER = ?
            ORDER BY ENCOUNTER_TIME, SCHEDULE_START_DATE;""",
      ( 'Kangaroo', ) )

   assert [
      (
         row[ 'SCHEDULE_START_DATE' ],
         row[ 'SCHEDULE_END_DATE' ],
         row[ 'ENCOUNTER_TIME' ],
      )
      for row in cur.fetchall()
   ] == [
      ( '2026-06-28', '2026-07-05', '10:00 AM' ),
      ( '2026-07-06', '2026-07-10', '10:00 AM' ),
      ( '2026-06-28', '2026-07-05', '3:30 PM' ),
      ( '2026-07-06', '2026-07-10', '3:30 PM' ),
   ]


def test_wild_encounter_occurrence_cancel_accepts_multiple_times(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '10:00 AM', '3:30 PM' ),
      message=None
   )

   assert WildEncounterCoordinator.cancel_wild_encounter_occurrence(
      wild_encounter_name='Kangaroo',
      date='2026-06-15',
      encounter_times=[ '10:00 AM', '3:30 PM' ] )

   encounters = WildEncounterCoordinator.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   kangaroo_times = sorted(
      item.start_time
      for item in encounters
      if item.name == 'Kangaroo'
   )

   assert kangaroo_times == [ '10:00 AM', '3:30 PM' ]
   assert all(
      not item.is_available
      for item in encounters
      if item.name == 'Kangaroo'
   )


def test_wild_encounter_schedule_end_updates_canonical_encounter_time_row(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   cur = db.conn.cursor()
   cur.execute(
      """   INSERT INTO WildEncounterSchedule (
               WILD_ENCOUNTER,
               SCHEDULE_START_DATE,
               ENCOUNTER_TIME,
               MONDAY,
               TUESDAY,
               WEDNESDAY,
               THURSDAY,
               FRIDAY,
               SATURDAY,
               SUNDAY
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
      (
         'Sunrise in Sumatra',
         '2026-06-01',
         '8:45 AM',
         1,
         0,
         0,
         0,
         0,
         0,
         0,
      ) )
   db.conn.commit()

   assert WildEncounterCoordinator.end_wild_encounter_schedule(
      wild_encounter_name='Sunrise in Sumatra',
      schedule_end_date='2026-06-14',
      encounter_times=[ '8:45 AM' ] )

   cur.execute(
      """   SELECT SCHEDULE_END_DATE, ENCOUNTER_TIME
            FROM WildEncounterSchedule
            WHERE WILD_ENCOUNTER = ?;""",
      ( 'Sunrise in Sumatra', ) )

   schedule_end_date, encounter_time = cur.fetchone()

   assert schedule_end_date == '2026-06-14'
   assert encounter_time == '8:45 AM'


def test_end_wild_encounter_schedule_uses_today_when_end_date_is_null(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row( '10:00 AM', monday=True, tuesday=True, wednesday=True, thursday=True, friday=True, saturday=True, sunday=True ),
         wire_schedule_row( '3:30 PM', monday=True, tuesday=True, wednesday=True, thursday=True, friday=True, saturday=True, sunday=True ),
      ],
      message=None
   )

   assert WildEncounterCoordinator.end_wild_encounter_schedule(
      wild_encounter_name='Kangaroo',
      schedule_end_date=None,
      encounter_times=[ '10:00 AM', '3:30 PM' ] )

   cur = db.conn.cursor()
   cur.execute(
      """   SELECT SCHEDULE_END_DATE, ENCOUNTER_TIME
            FROM WildEncounterSchedule
            WHERE WILD_ENCOUNTER = ?
            ORDER BY ENCOUNTER_TIME;""",
      ( 'Kangaroo', ) )

   rows = cur.fetchall()

   assert len( rows ) == 2
   assert rows[ 0 ][ 'SCHEDULE_END_DATE' ] == '2026-06-15'
   assert rows[ 0 ][ 'ENCOUNTER_TIME' ] == '10:00 AM'
   assert rows[ 1 ][ 'SCHEDULE_END_DATE' ] == '2026-06-15'
   assert rows[ 1 ][ 'ENCOUNTER_TIME' ] == '3:30 PM'


