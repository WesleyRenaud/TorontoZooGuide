from __future__ import annotations

from .transportation_record import TransportationRecord
from ...types import Row


def map_transportation_record( row: Row ) -> TransportationRecord:
   return TransportationRecord(
      name=row[ 'NAME' ],
      is_also_attraction=bool( row[ 'IS_ALSO_ATTRACTION' ] ),
      free_with_admission=bool( row[ 'FREE_WITH_ADMISSION' ] ),
      description=row[ 'DESCRIPTION' ],
      info_link=row[ 'INFO_LINK' ],
      hyperlink_text=row[ 'HYPERLINK_TEXT' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ],
      region=row[ 'REGION' ] )


def map_transportation_records(
      rows: list[ Row ] ) -> list[ TransportationRecord ]:
   return [
      map_transportation_record( row )
      for row in rows
   ]
