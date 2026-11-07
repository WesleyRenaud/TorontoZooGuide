from __future__ import annotations

from ..domain.attraction_info_link import AttractionInfoLink
from ...types import Types


class AttractionInfoLinkMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> AttractionInfoLink:
      return AttractionInfoLink(
         name=row[ 'NAME' ],
         info_link=row[ 'INFO_LINK' ] )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ AttractionInfoLink ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
