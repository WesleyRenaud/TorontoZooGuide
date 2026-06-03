from __future__ import annotations

from typing import Any

from ...animals.controllers.animal_controller import AnimalController
from ...attractions.controllers.attraction_controller import AttractionController
from .bulk_schedule_animals_warning import build_bulk_schedule_animals_not_enough_time_issue
from .bulk_schedule_exhibit_order import bulk_schedule_exhibit_rank
from ..data_access.itinerary import fetch_saved_itinerary
from ..data_access.itinerary_animal_record import ItineraryAnimalRecord
from ..data_access.itinerary_default_duration import fetch_enclosure_default_duration_minutes
from ..data_access.schedule_itinerary_item import update_itinerary_animal_schedule
from ...guardians.controllers.guardians_controller import GuardiansController
from .itinerary import build_current_itinerary
from .itinerary_save_issue import ItinerarySaveIssue
from .itinerary_save_result import ItinerarySaveResult
from .schedule_itinerary_item import _itinerary_controller_kwargs
from .schedule_itinerary_item import _resolve_schedule_window
from ..scheduling.resolve_schedule_slot import resolve_schedule_slot
from ..scheduling.time_block import collect_time_blocks_from_itinerary
from ..scheduling.time_block import time_block_from_schedule_times
from ..scheduling.time_block import TimeBlock
from ...shared.enums import ItineraryErrorType
from ...types import Connection
from ...types import ScheduleTimeKey
from ...wild_encounters.controllers.wild_encounter_controller import WildEncounterController


def is_itinerary_animal_unscheduled( animal_row: ItineraryAnimalRecord ) -> bool:
   return (
      animal_row.start_time is None
      or animal_row.end_time is None )


def sort_animals_for_bulk_schedule(
      animal_rows: list[ ItineraryAnimalRecord ],
) -> list[ ItineraryAnimalRecord ]:
   return sorted(
      animal_rows,
      key=lambda animal_row: (
         bulk_schedule_exhibit_rank( animal_row.exhibit ),
         animal_row.exhibit.lower(),
         animal_row.species.lower(),
      ) )


def bulk_schedule_animals(
      conn: Connection,
      *,
      animal_controller: type[ AnimalController ],
      attraction_controller: type[ AttractionController ],
      guardians_controller: type[ GuardiansController ],
      wild_encounter_controller: type[ WildEncounterController ],
      visit_date_temp: float | None = None,
) -> ItinerarySaveResult:
   itinerary_controller_kwargs = _itinerary_controller_kwargs(
      animal_controller=animal_controller,
      attraction_controller=attraction_controller,
      guardians_controller=guardians_controller,
      wild_encounter_controller=wild_encounter_controller,
      visit_date_temp=visit_date_temp )

   saved_itinerary = fetch_saved_itinerary( conn )
   window = _resolve_schedule_window(
      conn,
      saved_itinerary,
      **itinerary_controller_kwargs )

   if isinstance( window, ItinerarySaveResult ):
      return window

   anchor_minutes, day_end_minutes = window
   itinerary = build_current_itinerary(
      saved_itinerary,
      **itinerary_controller_kwargs )
   blockers = collect_time_blocks_from_itinerary( itinerary )

   unscheduled_animals = sort_animals_for_bulk_schedule( [
      animal_row
      for animal_row in saved_itinerary.animal_rows
      if is_itinerary_animal_unscheduled( animal_row )
   ] )

   if not unscheduled_animals:
      return ItinerarySaveResult(
         itinerary=build_current_itinerary(
            fetch_saved_itinerary( conn ),
            **itinerary_controller_kwargs ) )

   remaining_animals = _schedule_animals_in_order(
      conn,
      unscheduled_animals,
      blockers=blockers,
      anchor_minutes=anchor_minutes,
      day_end_minutes=day_end_minutes )

   issues: tuple[ ItinerarySaveIssue, ... ] = ()

   if remaining_animals:
      issues = (
         build_bulk_schedule_animals_not_enough_time_issue(
            remaining_animals ),
      )

   return ItinerarySaveResult(
      error_type=ItineraryErrorType.SUCCESS,
      issues=issues,
      itinerary=build_current_itinerary(
         fetch_saved_itinerary( conn ),
         **itinerary_controller_kwargs ) )


def _schedule_animals_in_order(
      conn: Connection,
      animals: list[ ItineraryAnimalRecord ],
      *,
      blockers: list[ TimeBlock ],
      anchor_minutes: int,
      day_end_minutes: int,
) -> list[ ItineraryAnimalRecord ]:
   cur = conn.cursor()

   try:
      for index, animal_row in enumerate( animals ):
         duration_minutes = fetch_enclosure_default_duration_minutes(
            conn,
            animal_row.species,
            animal_row.exhibit )

         if duration_minutes is None:
            return animals[ index: ]

         slot = resolve_schedule_slot(
            blockers,
            anchor_minutes,
            duration_minutes,
            day_end_minutes,
            start_time=None )

         if slot is None:
            return animals[ index: ]

         start_time, end_time = slot

         if not _persist_animal_schedule(
               cur,
               animal_row=animal_row,
               start_time=start_time,
               end_time=end_time ):
            return animals[ index: ]

         scheduled_block = time_block_from_schedule_times(
            start_time,
            end_time )

         if scheduled_block is not None:
            blockers.append( scheduled_block )

      conn.commit()
      return []

   finally:
      cur.close()


def _persist_animal_schedule(
      cur: Any,
      *,
      animal_row: ItineraryAnimalRecord,
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey,
) -> bool:
   return update_itinerary_animal_schedule(
      cur,
      species=animal_row.species,
      exhibit=animal_row.exhibit,
      start_time=start_time,
      end_time=end_time )
