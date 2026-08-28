from __future__ import annotations

from .itinerary_animal_mapper import ItineraryAnimalMapper
from .itinerary_animal_record import ItineraryAnimalRecord
from .itinerary_attraction_mapper import ItineraryAttractionMapper
from .itinerary_attraction_record import ItineraryAttractionRecord
from .itinerary_date_mapper import ItineraryDateMapper
from .itinerary_date_record import ItineraryDateRecord
from .itinerary_event_mapper import ItineraryEventMapper
from .itinerary_event_record import ItineraryEventRecord
from .itinerary_exhibit_provider import ItineraryExhibitProvider
from .itinerary_guardians_talk_mapper import ItineraryGuardiansTalkMapper
from .itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from .itinerary_transportation_leg_mapper import ItineraryTransportationLegMapper
from .itinerary_transportation_mapper import ItineraryTransportationMapper
from .itinerary_transportation_record import ItineraryTransportationRecord
from .itinerary_transportation_route_marker_provider import ItineraryTransportationRouteMarkerProvider
from .itinerary_wild_encounter_mapper import ItineraryWildEncounterMapper
from .itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from ...models.itinerary_transportation_leg import ItineraryTransportationLeg
from .saved_itinerary import SavedItinerary
from ...types import Types


class ItineraryProvider():
   @classmethod
   def fetch_itinerary_date_record( cls, conn: Types.Connection ) -> ItineraryDateRecord | None:
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

      return ItineraryDateMapper.map_record( date_row )


   @classmethod
   def fetch_itinerary_date( cls, conn: Types.Connection ) -> Types.DateKey | None:
      date_record = cls.fetch_itinerary_date_record( conn )

      if date_record == None or date_record.itinerary_date == None:
         return None

      return date_record.itinerary_date


   @classmethod
   def fetch_itinerary_animal_rows( cls, conn: Types.Connection ) -> list[ ItineraryAnimalRecord ]:
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

      return ItineraryAnimalMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_attraction_rows( cls, conn: Types.Connection ) -> list[ ItineraryAttractionRecord ]:
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

      return ItineraryAttractionMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_transportation_leg_rows(
         cls,
         conn: Types.Connection ) -> list[ ItineraryTransportationLeg ]:
      cur = conn.cursor()

      rows = cur.execute(
         """   SELECT
                  TRANSPORTATION,
                  ADDED_AS_ATTRACTION,
                  FROM_STATION,
                  TO_STATION,
                  START_TIME,
                  END_TIME
               FROM ItineraryTransportationLeg
               ORDER BY TRANSPORTATION, ADDED_AS_ATTRACTION, START_TIME;
         """ ).fetchall()

      cur.close()

      return ItineraryTransportationLegMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_transportation_rows(
         cls,
         conn: Types.Connection ) -> list[ ItineraryTransportationRecord ]:
      cur = conn.cursor()

      rows = cur.execute(
         """   SELECT
                  TRANSPORTATION,
                  OLD_LIKELIHOOD,
                  NEW_LIKELIHOOD,
                  ADDED_AS_ATTRACTION,
                  START_TIME,
                  END_TIME,
                  ROUTE,
                  BULK_TRANSIT_EVALUATED
               FROM ItineraryTransportation;
         """ ).fetchall()

      cur.close()

      return ItineraryTransportationMapper.map_records(
         rows,
         legs=cls.fetch_itinerary_transportation_leg_rows( conn ),
         route_markers=ItineraryTransportationRouteMarkerProvider.fetch_itinerary_transportation_route_markers( conn ),
      )


   @classmethod
   def fetch_itinerary_guardians_talk_rows( cls, conn: Types.Connection ) -> list[ ItineraryGuardiansTalkRecord ]:
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

      return ItineraryGuardiansTalkMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_wild_encounter_rows( cls, conn: Types.Connection ) -> list[ ItineraryWildEncounterRecord ]:
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

      return ItineraryWildEncounterMapper.map_records( rows )


   @classmethod
   def fetch_itinerary_event_rows( cls, conn: Types.Connection ) -> list[ ItineraryEventRecord ]:
      cur = conn.cursor()

      rows = cur.execute(
         """   SELECT
                  EVENT_TYPE,
                  START_TIME,
                  END_TIME
               FROM ItineraryEvent;
         """ ).fetchall()

      cur.close()

      return ItineraryEventMapper.map_records( rows )


   @classmethod
   def fetch_saved_itinerary( cls, conn: Types.Connection ) -> SavedItinerary:
      date_record = cls.fetch_itinerary_date_record( conn )

      if date_record == None or date_record.itinerary_date == None:
         return SavedItinerary(
            date_value=None,
            arrival_time=None,
            departure_time=None,
            selected_exhibits=[],
            animal_rows=[],
            attraction_rows=[],
            transportation_rows=[],
            guardians_talk_rows=[],
            wild_encounter_rows=[],
            event_rows=[] )

      return SavedItinerary(
         date_value=date_record.itinerary_date,
         arrival_time=date_record.arrival_time,
         departure_time=date_record.departure_time,
         selected_exhibits=ItineraryExhibitProvider.fetch_itinerary_exhibits( conn ),
         animal_rows=cls.fetch_itinerary_animal_rows( conn ),
         attraction_rows=cls.fetch_itinerary_attraction_rows( conn ),
         transportation_rows=cls.fetch_itinerary_transportation_rows( conn ),
         guardians_talk_rows=cls.fetch_itinerary_guardians_talk_rows( conn ),
         wild_encounter_rows=cls.fetch_itinerary_wild_encounter_rows( conn ),
         event_rows=cls.fetch_itinerary_event_rows( conn ) )
