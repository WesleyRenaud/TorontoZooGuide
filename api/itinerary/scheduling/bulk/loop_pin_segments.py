from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from ...data_access.itinerary_animal_record import ItineraryAnimalRecord
from ...routing.loop_schedule_pin import LoopSchedulePin
from ....walk_graph.master_route import default_master_route_loop_by_id
from ....walk_graph.master_route import viewing_spot_key_from_reference


@dataclass( frozen=True )
class LoopPinAnimalSegment:
   animals: list[ ItineraryAnimalRecord ]
   end_before_seconds: int
   anchor_at_end: bool


@dataclass( frozen=True )
class LoopPinGapStep:
   loop_pin: LoopSchedulePin


LoopPinScheduleStep = Union[
   LoopPinAnimalSegment,
   LoopPinGapStep,
]


def loop_pin_schedule_steps(
      animals: list[ ItineraryAnimalRecord ],
      *,
      loop_id: str,
      loop_pins: list[ LoopSchedulePin ],
      window_end_seconds: int,
   ) -> list[ LoopPinScheduleStep ]:
   animal_segments = split_animals_into_loop_pin_segments(
      animals,
      loop_id=loop_id,
      loop_pins=loop_pins )
   steps: list[ LoopPinScheduleStep ] = []

   for pin_index, loop_pin in enumerate( loop_pins ):
      before_pin_animals = animal_segments[ pin_index ]

      if before_pin_animals:
         steps.append(
            LoopPinAnimalSegment(
               animals=before_pin_animals,
               end_before_seconds=loop_pin.start_seconds,
               anchor_at_end=True,
            ) )

      steps.append( LoopPinGapStep( loop_pin=loop_pin ) )

   after_last_pin_animals = animal_segments[ len( loop_pins ) ]

   if after_last_pin_animals:
      steps.append(
         LoopPinAnimalSegment(
            animals=after_last_pin_animals,
            end_before_seconds=window_end_seconds,
            anchor_at_end=False,
         ) )

   return steps


def split_animals_into_loop_pin_segments(
      animals: list[ ItineraryAnimalRecord ],
      *,
      loop_id: str,
      loop_pins: list[ LoopSchedulePin ],
   ) -> list[ list[ ItineraryAnimalRecord ] ]:
   pin_boundaries = [
      loop_pin.viewing_spot_index
      for loop_pin in loop_pins
   ]
   segments: list[ list[ ItineraryAnimalRecord ] ] = [
      [] for _ in range( len( loop_pins ) + 1 )
   ]

   for animal_row in animals:
      viewing_spot_index = viewing_spot_index_for_animal_in_loop(
         loop_id,
         animal_row )
      segment_index = loop_pin_segment_index_for_viewing_spot(
         viewing_spot_index,
         pin_boundaries=pin_boundaries )
      segments[ segment_index ].append( animal_row )

   return segments


def loop_pin_segment_index_for_viewing_spot(
      viewing_spot_index: int | None,
      *,
      pin_boundaries: list[ int ],
   ) -> int:
   if viewing_spot_index is None:
      return len( pin_boundaries )

   for pin_index, pin_boundary in enumerate( pin_boundaries ):
      if viewing_spot_index <= pin_boundary:
         return pin_index

   return len( pin_boundaries )


def animals_before_first_loop_pin(
      animals: list[ ItineraryAnimalRecord ],
      *,
      loop_id: str,
      loop_pins: list[ LoopSchedulePin ],
   ) -> list[ ItineraryAnimalRecord ]:
   segments = split_animals_into_loop_pin_segments(
      animals,
      loop_id=loop_id,
      loop_pins=loop_pins )

   if not segments:
      return []

   return segments[ 0 ]


def viewing_spot_index_for_animal_in_loop(
      loop_id: str,
      animal_row: ItineraryAnimalRecord ) -> int | None:
   master_route_loop = default_master_route_loop_by_id().get( loop_id )

   if master_route_loop is None:
      return None

   animal_key = animal_row.viewing_spot_key()
   matching_indexes = [
      index
      for index, viewing_spot in enumerate( master_route_loop.viewing_spots )
      if viewing_spot_key_from_reference( viewing_spot ) == animal_key
   ]

   if not matching_indexes:
      return None

   return min( matching_indexes )
