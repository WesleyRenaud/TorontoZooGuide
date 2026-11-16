from __future__ import annotations

from ...types import Types
from ...walk_graph.domain.viewing_spot_reference import ViewingSpotReference


class EnclosureViewingMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> ViewingSpotReference:
      return ViewingSpotReference(
         species=row[ 'SPECIES' ],
         exhibit=row[ 'EXHIBIT' ],
         name=row[ 'NAME' ],
      )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ ViewingSpotReference ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
