from ... import zoo
from .itinerary_animal_mapper import map_itinerary_animal_records
from .itinerary_attraction_mapper import map_itinerary_attraction_records
from .itinerary_guardians_talk_mapper import map_itinerary_guardians_talk_records
from .itinerary_wild_encounter_mapper import map_itinerary_wild_encounter_records
from .saved_itinerary import SavedItinerary


def fetch_itinerary_date( conn ):
   cur = conn.cursor()

   date_row = cur.execute(
      """   SELECT ITINERARY_DATE
            FROM ItineraryDate
            LIMIT 1;
      """
   ).fetchone()

   cur.close()

   if date_row == None or date_row[ 'ITINERARY_DATE' ] == None:
      return None

   return zoo.ZooUtil.normalize_date_key( date_row[ 'ITINERARY_DATE' ] )


def fetch_itinerary_animal_rows( conn ):
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            FROM ItineraryAnimal;
      """ ).fetchall()

   cur.close()

   return map_itinerary_animal_records( rows )


def fetch_itinerary_attraction_rows( conn ):
   cur = conn.cursor()

   rows = cur.execute(
      """   SELECT
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            FROM ItineraryAttraction;
      """ ).fetchall()

   cur.close()

   return map_itinerary_attraction_records( rows )


def fetch_itinerary_guardians_talk_rows( conn ):
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


def fetch_itinerary_wild_encounter_rows( conn ):
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


def fetch_saved_itinerary( conn ):
   date_value = fetch_itinerary_date( conn )

   if date_value == None:
      return SavedItinerary(
         date_value=None,
         animal_rows=(),
         attraction_rows=(),
         guardians_talk_rows=(),
         wild_encounter_rows=() )

   return SavedItinerary(
      date_value=date_value,
      animal_rows=tuple( fetch_itinerary_animal_rows( conn ) ),
      attraction_rows=tuple( fetch_itinerary_attraction_rows( conn ) ),
      guardians_talk_rows=tuple( fetch_itinerary_guardians_talk_rows( conn ) ),
      wild_encounter_rows=tuple( fetch_itinerary_wild_encounter_rows( conn ) ) )
