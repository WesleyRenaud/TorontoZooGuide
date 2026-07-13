from __future__ import annotations

from .itinerary_animal_mapper import map_itinerary_animal_records
from .itinerary_animal_record import ItineraryAnimalRecord
from .itinerary_attraction_mapper import map_itinerary_attraction_records
from .itinerary_attraction_record import ItineraryAttractionRecord
from .itinerary_date_mapper import map_itinerary_date_record
from .itinerary_date_record import ItineraryDateRecord
from .itinerary_event_mapper import map_itinerary_event_records
from .itinerary_event_record import ItineraryEventRecord
from .itinerary_guardians_talk_mapper import map_itinerary_guardians_talk_records
from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from .itinerary_wild_encounter_mapper import map_itinerary_wild_encounter_records
from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from .saved_itinerary import SavedItinerary
from ...types import Connection, DateKey


def fetch_itinerary_date_record( conn: Connection ) -> ItineraryDateRecord | None:
   cur = conn.cursor()

   date_row = cur.execute(
      """   SELECT
               ITINERARY_DATE,
               ARRIVAL_TIME,
               DEPARTURE_TIME
            FROM ItineraryDate
            LIMIT 1;
      """
   ).fetchone()

   cur.close()

   return map_itinerary_date_record( date_row )


def fetch_itinerary_date( conn: Connection ) -> DateKey | None:
   date_record = fetch_itinerary_date_record( conn )

   if date_record == None or date_record.itinerary_date == None:
      return None

   return date_record.itinerary_date


def fetch_itinerary_animal_rows( conn: Connection ) -> list[ ItineraryAnimalRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               IS_ADDED,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            FROM ItineraryAnimal;
      """ ).fetchall()

   cur.close()

   return map_itinerary_animal_records( rows )


def fetch_itinerary_attraction_rows( conn: Connection ) -> list[ ItineraryAttractionRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               START_TIME,
               END_TIME
            FROM ItineraryAttraction;
      """ ).fetchall()

   cur.close()

   return map_itinerary_attraction_records( rows )


def fetch_itinerary_guardians_talk_rows( conn: Connection ) -> list[ ItineraryGuardiansTalkRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            FROM ItineraryGuardiansTalk;
      """ ).fetchall()

   cur.close()

   return map_itinerary_guardians_talk_records( rows )


def fetch_itinerary_wild_encounter_rows( conn: Connection ) -> list[ ItineraryWildEncounterRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            FROM ItineraryWildEncounter;
      """ ).fetchall()

   cur.close()

   return map_itinerary_wild_encounter_records( rows )


def fetch_itinerary_event_rows( conn: Connection ) -> list[ ItineraryEventRecord ]:
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               EVENT_TYPE,
               START_TIME,
               END_TIME
            FROM ItineraryEvent;
      """ ).fetchall()

   cur.close()

   return map_itinerary_event_records( rows )


def fetch_saved_itinerary( conn: Connection ) -> SavedItinerary:
   date_record = fetch_itinerary_date_record( conn )

   if date_record == None or date_record.itinerary_date == None:
      return SavedItinerary(
         date_value=None,
         arrival_time=None,
         departure_time=None,
         animal_rows=(),
         attraction_rows=(),
         guardians_talk_rows=(),
         wild_encounter_rows=(),
         event_rows=() )

   return SavedItinerary(
      date_value=date_record.itinerary_date,
      arrival_time=date_record.arrival_time,
      departure_time=date_record.departure_time,
      animal_rows=tuple( fetch_itinerary_animal_rows( conn ) ),
      attraction_rows=tuple( fetch_itinerary_attraction_rows( conn ) ),
      guardians_talk_rows=tuple( fetch_itinerary_guardians_talk_rows( conn ) ),
      wild_encounter_rows=tuple( fetch_itinerary_wild_encounter_rows( conn ) ),
      event_rows=tuple( fetch_itinerary_event_rows( conn ) ) )
