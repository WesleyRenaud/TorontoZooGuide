from __future__ import annotations

from typing import TYPE_CHECKING

from ...types import Connection, DateKey

if TYPE_CHECKING:
   from ..logic.wild_encounter_cancellation_input import WildEncounterCancellationInput
   from ..logic.wild_encounter_schedule_end_input import WildEncounterScheduleEndInput
   from ..logic.wild_encounter_schedule_input import WildEncounterScheduleInput

from .wild_encounter_mapper import map_wild_encounter_records
from .wild_encounter_record import WildEncounterRecord


def fetch_wild_encounter_names( conn: Connection ) -> list[ str ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  w.NAME
               FROM WildEncounter w;
         """ )

      return [
         row[ 'NAME' ]
         for row in data.fetchall()
      ]

   finally:
      cur.close()


def fetch_wild_encounter_records( conn: Connection ) -> list[ WildEncounterRecord ]:
   cur = conn.cursor()

   try:
      data = cur.execute(
         """   SELECT
                  w.NAME,
                  w.MEETING_SPOT,
                  w.LINK,
                  w.MAXIMUM_DURATION,
                  m.X_COORD,
                  m.Y_COORD
               FROM WildEncounter w
               JOIN WildEncounterMeetingSpot m
                  ON w.MEETING_SPOT = m.NAME;
         """ )

      return map_wild_encounter_records( data.fetchall() )

   finally:
      cur.close()
