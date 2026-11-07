from __future__ import annotations

from ..data_access.animal_off_display_record import AnimalOffDisplayRecord
from .seasonal_off_display_animal import SeasonalOffDisplayAnimal
from ...shared.date_values import DateValues
from .species_off_display_records import SpeciesOffDisplayRecords


class SeasonalOffDisplayAnimalBuilder():
   @classmethod
   def build(
         cls,
         species: list[ str ],
         records: list[ AnimalOffDisplayRecord ] ) -> list[ SeasonalOffDisplayAnimal ]:
      groups = SpeciesOffDisplayRecords.groups( species, records )
      return cls._listed( groups ) + cls._unlisted( species, records )


   @classmethod
   def _listed(
         cls,
         groups: list[ SpeciesOffDisplayRecords ] ) -> list[ SeasonalOffDisplayAnimal ]:
      built = []

      for group in groups:
         if group.records:
            built.extend(
               cls._off_display( group.species, record )
               for record in group.records
            )
         else:
            built.append( cls._on_display( group.species ) )

      return built


   @classmethod
   def _unlisted(
         cls,
         species: list[ str ],
         records: list[ AnimalOffDisplayRecord ] ) -> list[ SeasonalOffDisplayAnimal ]:
      listed = set( species )
      return [
         cls._off_display( record.species, record )
         for record in records
         if record.species not in listed
      ]


   @classmethod
   def _on_display( cls, name: str ) -> SeasonalOffDisplayAnimal:
      return SeasonalOffDisplayAnimal(
         name=name,
         is_off_display=False,
         start=None,
         end=None,
         off_for_season=False,
      )


   @classmethod
   def _off_display( cls, name: str, record: AnimalOffDisplayRecord ) -> SeasonalOffDisplayAnimal:
      return SeasonalOffDisplayAnimal(
         name=name,
         is_off_display=record.is_off_display,
         start=DateValues.parse_date_value( record.start ),
         end=DateValues.parse_date_value( record.end ),
         off_for_season=record.off_for_season,
      )
