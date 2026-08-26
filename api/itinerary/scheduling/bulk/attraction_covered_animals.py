from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ....attractions.data_access.attraction_animal_provider import AttractionAnimalProvider
from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ...data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from ...data_access.itinerary_provider import ItineraryProvider
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ...data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ....models import AnimalDiff
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import Cursor
from ....walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey


CoveredAnimalAttraction = tuple[ ItineraryAnimalRecord, str ]


@dataclass( frozen=True )
class RestoredAttractionCoveredAnimals:
   animals: list[ ItineraryAnimalRecord ]
   replacement_end_seconds: int | None


def viewing_spot_keys_to_cover_for_attractions(
      conn: Connection,
      attraction_names: list[ str ],
      animal_rows: list[ ItineraryAnimalRecord ],
   ) -> dict[ ViewingSpotNameKey, CoveredAnimalAttraction ]:
   animal_by_key = {
      animal_row.viewing_spot_key(): animal_row
      for animal_row in animal_rows
   }
   covered: dict[ ViewingSpotNameKey, CoveredAnimalAttraction ] = {}

   for attraction_name in attraction_names:
      for link in AttractionAnimalProvider.fetch_attraction_animal_links(
            conn,
            attraction_name ):
         spot_key = link.viewing_spot_key()
         animal_row = animal_by_key.get( spot_key )

         if animal_row is None:
            continue

         covered[ spot_key ] = ( animal_row, attraction_name )

   return covered


def apply_covered_by_attraction_schedules(
      conn: Connection,
      covered_by_attraction: dict[ ViewingSpotNameKey, CoveredAnimalAttraction ],
   ) -> None:
   if not covered_by_attraction:
      return

   attraction_by_name = {
      attraction_row.attraction: attraction_row
      for attraction_row in ItineraryProvider.fetch_saved_itinerary( conn ).attraction_rows
   }
   cur = conn.cursor()

   try:
      for animal_row, attraction_name in covered_by_attraction.values():
         attraction_row = attraction_by_name.get( attraction_name )

         if (
               attraction_row is None
               or attraction_row.start_time is None
               or attraction_row.end_time is None ):
            continue

         ScheduleItineraryItemProvider.update_itinerary_animal_cover_and_schedule(
            cur,
            species=animal_row.species,
            exhibit=animal_row.exhibit,
            enclosure_name=animal_row.enclosure_name,
            covered_by_talk=True,
            start_time=attraction_row.start_time,
            end_time=attraction_row.end_time )

      conn.commit()

   finally:
      cur.close()


def restore_covered_animals_after_attraction_removed(
      cur: Cursor,
      conn: Connection,
      *,
      attraction_name: str,
      attraction_block: TimeBlock,
      animal_rows: list[ ItineraryAnimalRecord ],
   ) -> RestoredAttractionCoveredAnimals:
   animal_by_key = {
      animal_row.viewing_spot_key(): animal_row
      for animal_row in animal_rows
   }
   restored: list[ ItineraryAnimalRecord ] = []
   replacement_end_seconds: int | None = None

   for link in AttractionAnimalProvider.fetch_attraction_animal_links(
         conn,
         attraction_name ):
      animal_row = animal_by_key.get( link.viewing_spot_key() )

      if animal_row is None or not animal_row.covered_by_talk:
         continue

      duration_seconds = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
         conn,
         animal_row.species,
         animal_row.exhibit,
         animal_row.enclosure_name )

      if duration_seconds is None:
         UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
            cur,
            species=animal_row.species,
            exhibit=animal_row.exhibit,
            enclosure_name=animal_row.enclosure_name )
         continue

      start_time = DateValues.schedule_time_key_from_seconds(
         attraction_block.start_seconds )
      end_time = DateValues.schedule_time_key_from_seconds(
         attraction_block.start_seconds + duration_seconds )

      ScheduleItineraryItemProvider.update_itinerary_animal_cover_and_schedule(
         cur,
         species=animal_row.species,
         exhibit=animal_row.exhibit,
         enclosure_name=animal_row.enclosure_name,
         covered_by_talk=False,
         start_time=start_time,
         end_time=end_time )
      restored.append( animal_row )
      replacement_end_seconds = max(
         attraction_block.start_seconds + duration_seconds,
         replacement_end_seconds or attraction_block.start_seconds )

   return RestoredAttractionCoveredAnimals(
      animals=restored,
      replacement_end_seconds=replacement_end_seconds )


def uncover_animals_for_removed_attractions(
      conn: Connection,
      animals: list[ AnimalDiff ],
      removed_attraction_rows: list[ ItineraryAttractionRecord ],
   ) -> list[ AnimalDiff ]:
   animals_by_spot = {
      animal.viewing_spot_key(): animal
      for animal in animals
   }

   for attraction_row in removed_attraction_rows:
      attraction_block = time_block_from_schedule_times(
         attraction_row.start_time,
         attraction_row.end_time )

      for link in AttractionAnimalProvider.fetch_attraction_animal_links(
            conn,
            attraction_row.attraction ):
         existing = animals_by_spot.get( link.viewing_spot_key() )

         if existing is None or not existing.covered_by_talk:
            continue

         if attraction_block is None:
            existing.covered_by_talk = False
            existing.start_time = None
            existing.end_time = None
            continue

         duration_seconds = ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds(
            conn,
            existing.species,
            existing.exhibit,
            existing.enclosure_name )

         if duration_seconds is None:
            existing.covered_by_talk = False
            existing.start_time = None
            existing.end_time = None
            continue

         existing.covered_by_talk = False
         existing.start_time = DateValues.schedule_time_key_from_seconds(
            attraction_block.start_seconds )
         existing.end_time = DateValues.schedule_time_key_from_seconds(
            attraction_block.start_seconds + duration_seconds )

   return animals


def merge_covered_viewing_spot_keys(
      *covered_maps: Mapping[ ViewingSpotNameKey, object ],
   ) -> set[ ViewingSpotNameKey ]:
   merged: set[ ViewingSpotNameKey ] = set()

   for covered_map in covered_maps:
      merged.update( covered_map )

   return merged
