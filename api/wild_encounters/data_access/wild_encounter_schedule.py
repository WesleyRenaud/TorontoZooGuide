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
