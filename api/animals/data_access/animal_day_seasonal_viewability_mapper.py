from __future__ import annotations

from .animal_day_seasonal_viewability_record import AnimalDaySeasonalViewabilityRecord
from ...types import Types


class AnimalDaySeasonalViewabilityMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AnimalDaySeasonalViewabilityRecord:
      return AnimalDaySeasonalViewabilityRecord(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         month=row[ 'MONTH' ],
         day=row[ 'DAY' ],
         value=row[ 'VALUE' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AnimalDaySeasonalViewabilityRecord ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
