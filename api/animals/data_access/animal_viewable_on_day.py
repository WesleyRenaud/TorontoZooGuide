from __future__ import annotations

from ...types import Connection, VisitDay, VisitMonth
from .animal_viewability_mapper import map_animal_viewability_rows
from .animal_viewability_record import AnimalViewabilityRecord


_FETCH_ANIMALS_VIEWABLE_ON_DAY_SQL = """   SELECT
                  a.SPECIES,
                  a.LATIN_NAME,
                  a.MIN_TEMPERATURE,
                  a.GENERAL_VIEWING_TIPS,
                  a.SEASONAL_VIEWING_TIPS,
                  a.IDENTIFICATION,
                  a.HABITAT_AND_RANGE,
                  a.DIET_AND_FEEDING,
                  a.BEHAVIOUR_AND_SOCIAL_LIFE,
                  a.ADAPTATIONS,
                  a.REPRODUCTION_AND_LIFE_CYCLE,
                  a.ANIMALS_AT_THE_ZOO,
                  e.EXHIBIT,
                  e.SEASONAL_VIEWING_SUMMARY,
                  e.SEASONAL_VIEWING_INFORMATION,
                  v.ENCLOSURE_TYPE,
                  v.SEASONALLY_OFF_DISPLAY_MESSAGE,
                  v.X_COORD,
                  v.Y_COORD,
                  s.IS_OFF_DISPLAY,
                  s.OFF_DISPLAY_MESSAGE,
                  s.OFF_DISPLAY_START,
                  s.OFF_DISPLAY_END,
                  vs.SCHEDULE_START_DATE,
                  vs.SCHEDULE_END_DATE,
                  vs.DAILY_START_TIME,
                  vs.DAILY_END_TIME,
                  vs.VIEWING_MESSAGE,
                  va.ALERT_MESSAGE,
                  va.ALERT_START_DATE,
                  va.ALERT_END_DATE,
                  es.IS_CLOSED,
                  es.CLOSED_MESSAGE,
                  es.CLOSED_START,
                  es.CLOSED_END,
                  COALESCE( adsvm.VALUE, 1.0 ) AS ANIMAL_DAY_SEASONAL_MULTIPLIER,
                  COALESCE( edsam.VALUE, 1.0 ) AS EXHIBIT_DAY_SEASONAL_AVAILABILITY_MULTIPLIER
               FROM Animal a
               JOIN Enclosure e
                  ON a.SPECIES = e.SPECIES
               JOIN EnclosureViewing v
                  ON e.SPECIES = v.SPECIES
                  AND e.EXHIBIT = v.EXHIBIT
               LEFT JOIN AnimalStatus s
                  ON e.SPECIES = s.SPECIES
                  AND e.EXHIBIT = s.EXHIBIT
               LEFT JOIN AnimalVisibilitySchedule vs
                  ON e.SPECIES = vs.SPECIES
                  AND e.EXHIBIT = vs.EXHIBIT
               LEFT JOIN AnimalViewingAlert va
                  ON e.SPECIES = va.SPECIES
                  AND e.EXHIBIT = va.EXHIBIT
               LEFT JOIN ExhibitStatus es
                  ON e.EXHIBIT = es.EXHIBIT
               LEFT JOIN AnimalDaySeasonalViewabilityMultiplier adsvm
                  ON e.SPECIES = adsvm.SPECIES
                  AND e.EXHIBIT = adsvm.EXHIBIT
                  AND adsvm.MONTH = ?
                  AND adsvm.DAY = ?
               LEFT JOIN ExhibitDaySeasonalAvailabilityMultiplier edsam
                  ON e.EXHIBIT = edsam.EXHIBIT
                  AND edsam.MONTH = ?
                  AND edsam.DAY = ?
         """


def normalize_exhibits_to_include(
      exhibits_to_include: list[ str ] | None ) -> list[ str ]:
   return [
      exhibit.strip() for exhibit in exhibits_to_include or []
      if isinstance( exhibit, str ) and exhibit.strip() != ''
   ]


def fetch_animals_viewable_on_day_records(
      conn: Connection,
      normalized_month: VisitMonth,
      normalized_day: VisitDay,
      exhibits_to_include: list[ str ] | None = None ) -> list[ AnimalViewabilityRecord ]:
   """Load joined animal / exhibit / viewing records for viewability on a calendar day."""
   cur = conn.cursor()
   sql = _FETCH_ANIMALS_VIEWABLE_ON_DAY_SQL
   exhibits_to_include = normalize_exhibits_to_include( exhibits_to_include )
   parameters = [
      normalized_month,
      normalized_day,
      normalized_month,
      normalized_day,
   ]

   if exhibits_to_include:
      exhibit_placeholders = ', '.join( '?' for _ in exhibits_to_include )
      sql = f'{ sql } WHERE e.EXHIBIT IN ({ exhibit_placeholders })'
      parameters.extend( exhibits_to_include )

   try:
      data = cur.execute(
         f'{ sql };',
         parameters )

      return map_animal_viewability_rows( data.fetchall() )

   finally:
      cur.close()
