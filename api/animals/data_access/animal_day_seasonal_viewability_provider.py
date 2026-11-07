from __future__ import annotations

from .animal_day_seasonal_viewability_mapper import AnimalDaySeasonalViewabilityMapper
from .animal_day_seasonal_viewability_record import AnimalDaySeasonalViewabilityRecord
from ...types import Types


class AnimalDaySeasonalViewabilityProvider():
   @classmethod
   def fetch_records( cls, conn: Types.Connection ) -> list[ AnimalDaySeasonalViewabilityRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     SPECIES,
                     EXHIBIT,
                     MONTH,
                     DAY,
                     VALUE
                  FROM AnimalDaySeasonalViewabilityMultiplier;
            """ )

         return AnimalDaySeasonalViewabilityMapper.map_records( data.fetchall() )

      finally:
         cur.close()
