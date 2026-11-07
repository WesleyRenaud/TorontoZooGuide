from __future__ import annotations

from ..data_access.exhibit_closure_record import ExhibitClosureRecord
from .seasonal_exhibit import SeasonalExhibit
from ...shared.date_values import DateValues


class SeasonalExhibitBuilder():
   @classmethod
   def build(
         cls,
         exhibits: list[ str ],
         closure_records: list[ ExhibitClosureRecord ] ) -> list[ SeasonalExhibit ]:
      closures = cls._closures( closure_records )
      return cls._listed( exhibits, closures ) + cls._unlisted( exhibits, closures )


   @classmethod
   def _closures(
         cls,
         closure_records: list[ ExhibitClosureRecord ] ) -> dict[ str, ExhibitClosureRecord ]:
      return {
         record.exhibit: record
         for record in closure_records
         if record.closed_start != None
      }


   @classmethod
   def _listed(
         cls,
         exhibits: list[ str ],
         closures: dict[ str, ExhibitClosureRecord ] ) -> list[ SeasonalExhibit ]:
      return [
         cls._closure( name, closures[ name ] ) if name in closures else cls._open( name )
         for name in exhibits
      ]


   @classmethod
   def _unlisted(
         cls,
         exhibits: list[ str ],
         closures: dict[ str, ExhibitClosureRecord ] ) -> list[ SeasonalExhibit ]:
      listed = set( exhibits )
      return [
         cls._closure( name, record )
         for name, record in closures.items()
         if name not in listed
      ]


   @classmethod
   def _open( cls, name: str ) -> SeasonalExhibit:
      return SeasonalExhibit(
         name=name,
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      )


   @classmethod
   def _closure( cls, name: str, record: ExhibitClosureRecord ) -> SeasonalExhibit:
      return SeasonalExhibit(
         name=name,
         is_closed=True,
         start=DateValues.parse_date_value( record.closed_start ),
         end=DateValues.parse_date_value( record.closed_end ),
         closed_for_season=record.is_closed_for_season,
      )
