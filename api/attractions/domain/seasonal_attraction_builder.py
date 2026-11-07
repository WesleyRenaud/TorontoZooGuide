from __future__ import annotations

from .attraction_info_link import AttractionInfoLink
from ..data_access.attraction_closure_record import AttractionClosureRecord
from .seasonal_attraction import SeasonalAttraction
from ...shared.date_values import DateValues


class SeasonalAttractionBuilder():
   @classmethod
   def build(
         cls,
         attractions: list[ AttractionInfoLink ],
         closure_records: list[ AttractionClosureRecord ] ) -> list[ SeasonalAttraction ]:
      closures = {
         record.attraction: record
         for record in closure_records
         if record.closed_start != None
      }
      listed = { attraction.name for attraction in attractions }
      built = [
         cls._closure( attraction.name, closures[ attraction.name ], attraction.info_link )
         if attraction.name in closures
         else cls._open( attraction )
         for attraction in attractions
      ]

      for name, record in closures.items():
         if name in listed:
            continue

         built.append( cls._closure( name, record ) )

      return built


   @classmethod
   def _open( cls, attraction: AttractionInfoLink ) -> SeasonalAttraction:
      return SeasonalAttraction(
         name=attraction.name,
         info_link=attraction.info_link,
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      )


   @classmethod
   def _closure(
         cls,
         name: str,
         record: AttractionClosureRecord,
         info_link: str = '' ) -> SeasonalAttraction:
      return SeasonalAttraction(
         name=name,
         info_link=info_link,
         is_closed=True,
         start=DateValues.parse_date_value( record.closed_start ),
         end=DateValues.parse_date_value( record.closed_end ),
         closed_for_season=record.is_closed_for_season,
      )
