from __future__ import annotations

from ..domain.exhibit_season_status import ExhibitSeasonStatus
from ...shared.date_values import DateValues
from ...types import Types


class ExhibitSeasonStatusMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ExhibitSeasonStatus:
      return ExhibitSeasonStatus(
         exhibit=row[ 'EXHIBIT' ],
         is_closed=bool( row[ 'IS_CLOSED' ] ),
         start=DateValues.parse_date_value( row[ 'CLOSED_START' ] ),
         end=DateValues.parse_date_value( row[ 'CLOSED_END' ] ),
         closed_for_season=bool( row[ 'CLOSED_FOR_SEASON' ] ),
      )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ExhibitSeasonStatus ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
