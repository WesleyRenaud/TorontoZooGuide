from .wild_encounter_cancellation_mapper import map_wild_encounter_cancellation_records
from .wild_encounter_schedule_mapper import map_wild_encounter_schedule_record
from .wild_encounter_schedule_mapper import map_wild_encounter_schedule_records


def fetch_wild_encounter_schedule_records( conn, target_date ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.MEETING_SPOT,
                  w.LINK,
                  w.MAXIMUM_DURATION,
                  m.X_COORD,
                  m.Y_COORD,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.ENCOUNTER_TIME,
                  c.WILD_ENCOUNTER IS NOT NULL AS IS_CANCELLED
               FROM WildEncounter w
               JOIN WildEncounterMeetingSpot m
                  ON w.MEETING_SPOT = m.NAME
               JOIN WildEncounterSchedule s
                  ON w.NAME = s.WILD_ENCOUNTER
               LEFT JOIN WildEncounterCancellation c
                  ON c.WILD_ENCOUNTER = s.WILD_ENCOUNTER
                  AND c.CANCELLATION_DATE = ?
                  AND c.ENCOUNTER_TIME = s.ENCOUNTER_TIME;
         """,
         ( target_date, ) )

      return map_wild_encounter_schedule_records( data.fetchall() )

   finally:
      cur.close()


def fetch_wild_encounter_schedule_record_for_occurrences( conn, wild_encounter ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.MEETING_SPOT,
                  w.LINK,
                  w.MAXIMUM_DURATION,
                  m.X_COORD,
                  m.Y_COORD,
                  s.SCHEDULE_START_DATE,
                  s.SCHEDULE_END_DATE,
                  s.MONDAY,
                  s.TUESDAY,
                  s.WEDNESDAY,
                  s.THURSDAY,
                  s.FRIDAY,
                  s.SATURDAY,
                  s.SUNDAY,
                  s.ENCOUNTER_TIME,
                  0 AS IS_CANCELLED
               FROM WildEncounter w
               JOIN WildEncounterMeetingSpot m
                  ON w.MEETING_SPOT = m.NAME
               JOIN WildEncounterSchedule s
                  ON w.NAME = s.WILD_ENCOUNTER
               WHERE s.WILD_ENCOUNTER = ?;
         """,
         ( wild_encounter, ) )

      row = data.fetchone()

      if row == None:
         return None

      return map_wild_encounter_schedule_record( row )

   finally:
      cur.close()


def fetch_wild_encounter_cancellation_records( conn, wild_encounter ):
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  CANCELLATION_DATE,
                  ENCOUNTER_TIME
               FROM WildEncounterCancellation
               WHERE WILD_ENCOUNTER = ?;
         """,
         ( wild_encounter, ) )

      return map_wild_encounter_cancellation_records( data.fetchall() )

   finally:
      cur.close()



def save_wild_encounter_schedule( conn, schedule ):
   cur = conn.cursor()

   try:
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
                  SUNDAY,
                  SCHEDULE_MESSAGE
               )
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(WILD_ENCOUNTER) DO UPDATE SET
                  SCHEDULE_START_DATE = excluded.SCHEDULE_START_DATE,
                  SCHEDULE_END_DATE = excluded.SCHEDULE_END_DATE,
                  ENCOUNTER_TIME = excluded.ENCOUNTER_TIME,
                  MONDAY = excluded.MONDAY,
                  TUESDAY = excluded.TUESDAY,
                  WEDNESDAY = excluded.WEDNESDAY,
                  THURSDAY = excluded.THURSDAY,
                  FRIDAY = excluded.FRIDAY,
                  SATURDAY = excluded.SATURDAY,
                  SUNDAY = excluded.SUNDAY,
                  SCHEDULE_MESSAGE = excluded.SCHEDULE_MESSAGE;
         """,
         (
            schedule.wild_encounter,
            schedule.start_date,
            schedule.end_date,
            schedule.encounter_time,
            schedule.monday,
            schedule.tuesday,
            schedule.wednesday,
            schedule.thursday,
            schedule.friday,
            schedule.saturday,
            schedule.sunday,
            schedule.message,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()



def save_wild_encounter_schedule_end( conn, schedule_end ):
   cur = conn.cursor()

   try:
      cur.execute(
         """   UPDATE WildEncounterSchedule
               SET SCHEDULE_END_DATE = ?
               WHERE WILD_ENCOUNTER = ?;
         """,
         (
            schedule_end.schedule_end_date,
            schedule_end.wild_encounter,
         ) )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()
