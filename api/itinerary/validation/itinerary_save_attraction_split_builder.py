from __future__ import annotations

from ..data_access.attraction_also_transportation_provider import AttractionAlsoTransportationProvider
from ...types import Connection


class ItinerarySaveAttractionSplitBuilder():
   @classmethod
   def split_names(
         cls,
         conn: Connection,
         attraction_names: list[ str ],
   ) -> tuple[ list[ str ], list[ str ] ]:
      also_transportation_names = (
         AttractionAlsoTransportationProvider.fetch_also_transportation_attraction_names(
            conn ) )
      plain_attractions: list[ str ] = []
      transportations: list[ str ] = []

      for name in attraction_names:
         if name in also_transportation_names:
            transportations.append( name )
         else:
            plain_attractions.append( name )

      return plain_attractions, transportations
