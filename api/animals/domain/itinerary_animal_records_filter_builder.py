from __future__ import annotations

from ..data_access.animal_viewability_record import AnimalViewabilityRecord


class ItineraryAnimalRecordsFilterBuilder():
   @classmethod
   def filter(
         cls,
         animal_records: list[ AnimalViewabilityRecord ],
      ) -> list[ AnimalViewabilityRecord ]:
      return [
         animal_record
         for animal_record in animal_records
         if not animal_record.is_zoomobile_only
      ]
