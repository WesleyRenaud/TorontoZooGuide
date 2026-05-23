from __future__ import annotations

from collections.abc import Iterable

from ... import zoo
from ...types import Row


def map_event_site_record( row: Row ) -> zoo.EventSite:
   return zoo.EventSite(
      name=row[ 'NAME' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_event_site_records( rows: Iterable[ Row ] ) -> list[ zoo.EventSite ]:
   return [
      map_event_site_record( row )
      for row in rows
   ]
