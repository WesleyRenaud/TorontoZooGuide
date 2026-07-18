from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..core.time_block import TimeBlock
from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...data_access.itinerary_default_duration import fetch_enclosure_viewing_default_duration_seconds
from ...data_access.schedule_itinerary_item import update_itinerary_animal_cover_and_schedule
from ...data_access.unschedule_itinerary_item import clear_itinerary_animal_schedule
from ....guardians.data_access.guardians_talk_animal import fetch_guardians_talk_animal_links
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....shared.calendar_dates import DateValues
from ....types import Connection
from ....types import Cursor
from ....walk_graph.domain.viewing_spot_name_key import ViewingSpotNameKey


CoveredAnimalPin = tuple[ ItineraryAnimalRecord, LoopSchedulePin ]


@dataclass( frozen=True )
class RestoredTalkCoveredAnimals:
   animals: list[ ItineraryAnimalRecord ]
   replacement_end_seconds: int | None


def viewing_spot_keys_to_cover_for_loop_pins(
      conn: Connection,
      loop_pins: list[ LoopSchedulePin ],
      animal_rows: list[ ItineraryAnimalRecord ],
   ) -> dict[ ViewingSpotNameKey, CoveredAnimalPin ]:
   animal_by_key = {
      animal_row.viewing_spot_key(): animal_row
      for animal_row in animal_rows
   }
   covered: dict[ ViewingSpotNameKey, CoveredAnimalPin ] = {}

   for loop_pin in loop_pins:
      talk_name = loop_pin.stop.item_key

      for link in fetch_guardians_talk_animal_links( conn, talk_name ):
         spot_key = link.viewing_spot_key()
         animal_row = animal_by_key.get( spot_key )

         if animal_row is None:
            continue

         covered[ spot_key ] = ( animal_row, loop_pin )

   return covered


def apply_covered_by_talk_schedules(
      conn: Connection,
      covered_by_pin: dict[ ViewingSpotNameKey, CoveredAnimalPin ],
   ) -> None:
   if not covered_by_pin:
      return

   cur = conn.cursor()

   try:
      for animal_row, loop_pin in covered_by_pin.values():
         update_itinerary_animal_cover_and_schedule(
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

   for link in fetch_guardians_talk_animal_links( conn, talk_name ):
      animal_row = animal_by_key.get( link.viewing_spot_key() )

      if animal_row is None or not animal_row.covered_by_talk:
         continue

      clear_itinerary_animal_schedule(
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

   for link in fetch_guardians_talk_animal_links( conn, talk_name ):
      animal_row = animal_by_key.get( link.viewing_spot_key() )

      if animal_row is None or not animal_row.covered_by_talk:
         continue

      duration_seconds = fetch_enclosure_viewing_default_duration_seconds(
         conn,
         animal_row.species,
         animal_row.exhibit,
         animal_row.enclosure_name )

      if duration_seconds is None:
         clear_itinerary_animal_schedule(
            cur,
            species=animal_row.species,
            exhibit=animal_row.exhibit,
            enclosure_name=animal_row.enclosure_name )
         continue

      start_time = DateValues.schedule_time_key_from_seconds(
         talk_block.start_seconds )
      end_time = DateValues.schedule_time_key_from_seconds(
         talk_block.start_seconds + duration_seconds )

      update_itinerary_animal_cover_and_schedule(
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


def filter_animals_excluding_covered(
      animals: list[ ItineraryAnimalRecord ],
      covered_keys: Mapping[ ViewingSpotNameKey, CoveredAnimalPin ],
   ) -> list[ ItineraryAnimalRecord ]:
   return [
      animal
      for animal in animals
      if animal.viewing_spot_key() not in covered_keys
   ]
