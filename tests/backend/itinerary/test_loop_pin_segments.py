from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.loop_pin_segments import loop_pin_schedule_steps
from api.itinerary.scheduling.bulk.loop_pin_segments import loop_pin_segment_index_for_viewing_spot
from api.itinerary.scheduling.bulk.loop_pin_segments import LoopPinGapStep
from api.itinerary.scheduling.bulk.loop_pin_segments import LoopPinStopSegment
from api.itinerary.scheduling.bulk.loop_pin_segments import split_stops_into_loop_pin_segments
from api.shared.enums import ScheduleItemKind


def _animal_record(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> ItineraryAnimalRecord:
   return ItineraryAnimalRecord(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      old_likelihood=None,
      new_likelihood=100,
   )


def _hyena_loop_pin() -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=5,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Spotted Hyena',
         walk_node_ids=( 'v-0000', ),
         is_fixed_time=True,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
      start_seconds=46800,
      end_seconds=48600,
   )


def test_loop_pin_segment_index_places_animals_before_and_after_pin() -> None:
   assert loop_pin_segment_index_for_viewing_spot(
      3,
      pin_boundaries=[ 5 ] ) == 0
   assert loop_pin_segment_index_for_viewing_spot(
      5,
      pin_boundaries=[ 5 ] ) == 0
   assert loop_pin_segment_index_for_viewing_spot(
      20,
      pin_boundaries=[ 5 ] ) == 1
   assert loop_pin_segment_index_for_viewing_spot(
      None,
      pin_boundaries=[ 5 ] ) == 1


def test_split_stops_into_loop_pin_segments_groups_savanna_animals() -> None:
   loop_id = 'africa_savanna_canadian_domain'
   loop_pin = _hyena_loop_pin()
   penguin = _animal_record(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
   )
   cheetah = _animal_record(
      species='Cheetah',
      exhibit='Africa Savanna',
   )

   segments = split_stops_into_loop_pin_segments(
      [ cheetah, penguin ],
      loop_id=loop_id,
      loop_pins=[ loop_pin ],
   )

   assert [ animal.species for animal in segments[ 0 ] ] == [ 'African Penguin' ]
   assert [ animal.species for animal in segments[ 1 ] ] == [ 'Cheetah' ]


def test_loop_pin_schedule_steps_alternates_segments_and_gaps() -> None:
   loop_id = 'africa_savanna_canadian_domain'
   loop_pin = _hyena_loop_pin()
   penguin = _animal_record(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor',
   )
   cheetah = _animal_record(
      species='Cheetah',
      exhibit='Africa Savanna',
   )
   window_end_seconds = 61200

   steps = loop_pin_schedule_steps(
      [ penguin, cheetah ],
      loop_id=loop_id,
      loop_pins=[ loop_pin ],
      window_end_seconds=window_end_seconds,
   )

   assert len( steps ) == 3
   assert isinstance( steps[ 0 ], LoopPinStopSegment )
   assert [ animal.species for animal in steps[ 0 ].stops ] == [ 'African Penguin' ]
   assert steps[ 0 ].end_before_seconds == loop_pin.start_seconds
   assert steps[ 0 ].anchor_at_end is True
   assert isinstance( steps[ 1 ], LoopPinGapStep )
   assert steps[ 1 ].loop_pin is loop_pin
   assert isinstance( steps[ 2 ], LoopPinStopSegment )
   assert [ animal.species for animal in steps[ 2 ].stops ] == [ 'Cheetah' ]
   assert steps[ 2 ].end_before_seconds == window_end_seconds
   assert steps[ 2 ].anchor_at_end is False


def _attraction_record( name: str ) -> ItineraryAttractionRecord:
   return ItineraryAttractionRecord(
      attraction=name,
      old_likelihood=None,
      new_likelihood=100,
   )


def test_split_stops_into_loop_pin_segments_keeps_woven_attraction_with_post_pin_animals() -> None:
   loop_id = 'australasia'
   kangaroo = _animal_record(
      species='Western Grey Kangaroo',
      exhibit='Australasia Outdoor',
   )
   walk_thru = _attraction_record( 'Kangaroo Walk-Thru' )
   tiger = _animal_record(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
   )
   # Pin boundary at kangaroo (index 43): walk-thru (44) and tiger (45) fall after.
   loop_pin = LoopSchedulePin(
      loop_id=loop_id,
      viewing_spot_index=43,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key='Western Grey Kangaroo',
         walk_node_ids=( 'v-0000', ),
         is_fixed_time=True,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
      start_seconds=46800,
      end_seconds=48600,
   )

   segments = split_stops_into_loop_pin_segments(
      [ kangaroo, walk_thru, tiger ],
      loop_id=loop_id,
      loop_pins=[ loop_pin ],
   )

   assert [
      stop.attraction
      if isinstance( stop, ItineraryAttractionRecord )
      else stop.species
      for stop in segments[ 0 ]
   ] == [ 'Western Grey Kangaroo' ]
   assert [
      stop.attraction
      if isinstance( stop, ItineraryAttractionRecord )
      else stop.species
      for stop in segments[ 1 ]
   ] == [ 'Kangaroo Walk-Thru', 'Amur Tiger' ]
