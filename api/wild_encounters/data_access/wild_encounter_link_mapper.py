from __future__ import annotations

from ..domain.wild_encounter_link import WildEncounterLink
from ...types import Types


class WildEncounterLinkMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> WildEncounterLink:
      return WildEncounterLink(
         name=row[ 'NAME' ],
         link=( row[ 'LINK' ] or '' ).strip() )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ WildEncounterLink ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
