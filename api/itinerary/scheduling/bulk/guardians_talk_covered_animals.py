from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass

from ..core.time_block import time_block_from_schedule_times
from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration_provider import ItineraryDefaultDurationProvider
from ...data_access.schedule_itinerary_item_provider import ScheduleItineraryItemProvider
from ...data_access.unschedule_itinerary_item_provider import UnscheduleItineraryItemProvider
from ....guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from ....models import AnimalDiff
from ....models import GuardiansTalkDiff
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import Cursor
from ....walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey


CoveredAnimalTalk = tuple[ ItineraryAnimalRecord, LoopSchedulePin ]


@dataclass( frozen=True )
class RestoredTalkCoveredAnimals:
   animals: list[ ItineraryAnimalRecord ]
   replacement_end_seconds: int | None


def viewing_spot_keys_to_cover_for_loop_pins(
      conn: Connection,
      loop_pins: list[ LoopSchedulePin ],
      animal_rows: list[ ItineraryAnimalRecord ],
   ) -> dict[ ViewingSpotNameKey, CoveredAnimalTalk ]:
   animal_by_key = {
      animal_row.viewing_spot_key(): animal_row
      for animal_row in animal_rows
   }
   covered: dict[ ViewingSpotNameKey, CoveredAnimalTalk ] = {}

   for loop_pin in loop_pins:
      talk_name = loop_pin.stop.item_key

      for link in GuardiansTalkAnimalProvider.fetch_animal_links( conn, talk_name ):
         spot_key = link.viewing_spot_key()
         animal_row = animal_by_key.get( spot_key )

         if animal_row is None:
            continue

         covered[ spot_key ] = ( animal_row, loop_pin )

   return covered


def apply_covered_by_talk_schedules(
      conn: Connection,
      covered_by_talk: dict[ ViewingSpotNameKey, CoveredAnimalTalk ],
   ) -> None:
   if not covered_by_talk:
      return

   cur = conn.cursor()

   try:
      for animal_row, loop_pin in covered_by_talk.values():
         ScheduleItineraryItemProvider.update_itinerary_animal_cover_and_schedule(
            cur,
            species=animal_row.species,
            exhibit=animal_row.exhibit,
            enclosure_name=animal_row.enclosure_name,
            covered_by_talk=True,
            start_time=loop_pin.stop.start_time,
            end_time=loop_pin.stop.end_time )

      conn.commit()

   finally:
      cur.close()


def uncover_animals_for_talk(
      cur: Cursor,
      conn: Connection,
      *,
      talk_name: str,
      animal_rows: list[ ItineraryAnimalRecord ],
   ) -> list[ ItineraryAnimalRecord ]:
   animal_by_key = {
      animal_row.viewing_spot_key(): animal_row
      for animal_row in animal_rows
   }
   uncovered: list[ ItineraryAnimalRecord ] = []

   for link in GuardiansTalkAnimalProvider.fetch_animal_links( conn, talk_name ):
      animal_row = animal_by_key.get( link.viewing_spot_key() )

      if animal_row is None or not animal_row.covered_by_talk:
         continue

      UnscheduleItineraryItemProvider.clear_itinerary_animal_schedule(
         cur,
         species=animal_row.species,
         exhibit=animal_row.exhibit,
         enclosure_name=animal_row.enclosure_name )
      uncovered.append( animal_row )

   return uncovered


def restore_covered_animals_after_talk_removed(
      cur: Cursor,
      conn: Connection,
      *,
      talk_name: str,
      talk_block: TimeBlock,
      animal_rows: list[ ItineraryAnimalRecord ],
   ) -> RestoredTalkCoveredAnimals:
   animal_by_key = {
      animal_row.viewing_spot_key(): animal_row
      for animal_row in animal_rows
   }
   restored: list[ ItineraryAnimalRecord ] = []
   replacement_end_seconds: int | None = None

   for link in GuardiansTalkAnimalProvider.fetch_animal_links( conn, talk_name ):
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
         talk_block.start_seconds )
      end_time = DateValues.schedule_time_key_from_seconds(
         talk_block.start_seconds + duration_seconds )

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
         talk_block.start_seconds + duration_seconds,
         replacement_end_seconds or talk_block.start_seconds )

   return RestoredTalkCoveredAnimals(
      animals=restored,
      replacement_end_seconds=replacement_end_seconds )


def uncover_animals_for_unavailable_talks(
      conn: Connection,
      animals: list[ AnimalDiff ],
      guardians_talks: list[ GuardiansTalkDiff ],
   ) -> list[ AnimalDiff ]:
   animals_by_spot = {
      animal.viewing_spot_key(): animal
      for animal in animals
   }

   for talk in guardians_talks:
      if not talk.is_deleted:
         continue

      talk_block = time_block_from_schedule_times(
         talk.start_time,
         talk.end_time )

      if talk_block is None:
         continue

      for link in GuardiansTalkAnimalProvider.fetch_animal_links( conn, talk.name ):
         existing = animals_by_spot.get( link.viewing_spot_key() )

         if existing is None or not existing.covered_by_talk:
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
            talk_block.start_seconds )
         existing.end_time = DateValues.schedule_time_key_from_seconds(
            talk_block.start_seconds + duration_seconds )

   return animals


def filter_animals_excluding_covered(
      animals: list[ ItineraryAnimalRecord ],
      covered_keys: Collection[ ViewingSpotNameKey ],
   ) -> list[ ItineraryAnimalRecord ]:
   return [
      animal
      for animal in animals
      if animal.viewing_spot_key() not in covered_keys
   ]
