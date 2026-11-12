from __future__ import annotations

from ..domain.exhibit_season import ExhibitSeason
from ...types import Types


class ExhibitSeasonMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ExhibitSeason:
      return ExhibitSeason(
         row[ 'OPEN_START_MONTH' ],
         row[ 'OPEN_END_MONTH' ],
         row[ 'NAME' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ExhibitSeason ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
