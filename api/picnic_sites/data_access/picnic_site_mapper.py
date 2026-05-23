from __future__ import annotations

from collections.abc import Iterable

from ... import zoo
from ...types import Row


def map_picnic_site_record( row: Row ) -> zoo.PicnicSite:
   return zoo.PicnicSite(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_picnic_site_records( rows: Iterable[ Row ] ) -> list[ zoo.PicnicSite ]:
   return [
      map_picnic_site_record( row )
      for row in rows
   ]
