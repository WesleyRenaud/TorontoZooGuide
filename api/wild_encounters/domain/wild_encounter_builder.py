from __future__ import annotations

from ..data_access.wild_encounter_record import WildEncounterRecord
from ...models import WildEncounter
from .wild_encounter_include_filter import WildEncounterIncludeFilter


class WildEncounterBuilder():
   @classmethod
   def _record_to_model( cls, record: WildEncounterRecord ) -> WildEncounter:
      return WildEncounter(
         name=record.name,
         meeting_spot=record.meeting_spot,
         link=record.link,
         maximum_duration=record.maximum_duration,
         x_coord=record.x_coord,
         y_coord=record.y_coord,
         region=record.region )


   @classmethod
   def build_details(
         cls,
         wild_encounter_records: list[ WildEncounterRecord ],
         wild_encounters_to_include: list[ str ] | None = None ) -> list[ WildEncounter ]:
      include_filter = WildEncounterIncludeFilter.from_optional_list(
         wild_encounters_to_include )

      if include_filter.should_return_empty():
         return []

      wild_encounters: list[ WildEncounter ] = []

      for record in wild_encounter_records:
         if not include_filter.allows_wild_encounter_name( record.name ):
            continue

         wild_encounters.append( cls._record_to_model( record ) )

      wild_encounters.sort( key=lambda w: ( w.name or '' ).lower() )

      return wild_encounters
