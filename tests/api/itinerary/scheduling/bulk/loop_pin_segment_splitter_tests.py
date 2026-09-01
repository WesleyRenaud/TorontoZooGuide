from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.loop_pin_gap_step import LoopPinGapStep
from api.itinerary.scheduling.bulk.loop_pin_segment_splitter import LoopPinSegmentSplitter
from api.itinerary.scheduling.bulk.loop_pin_stop_segment import LoopPinStopSegment
from api.itinerary.scheduling.bulk.loop_schedule_stop import LoopScheduleStop
from api.shared.enums import ScheduleItemKind


AFRICA_LOOP_ID = 'africa_savanna_canadian_domain'
AUSTRALASIA_LOOP_ID = 'australasia'

HYENA_PIN_BOUNDARY = 5
GRIZZLY_ENCOUNTER_PIN_BOUNDARY = 6
KANGAROO_PIN_BOUNDARY = 43

VIEWING_SPOT_INDEX_BY_ANIMAL = {
   ( 'African Penguin', 'Africa Savanna', 'Outdoor' ): 3,
   ( 'Spotted Hyena', 'Africa Savanna', None ): 5,
   ( 'Cheetah', 'Africa Savanna', None ): 20,
   ( 'Western Grey Kangaroo', 'Australasia Outdoor', None ): 43,
   ( 'Amur Tiger', 'Eurasia Wilds', None ): 45,
}

VIEWING_SPOT_INDEX_BY_ATTRACTION = {
   'Kangaroo Walk-Thru': 44,
}


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


def _attraction_record( name: str ) -> ItineraryAttractionRecord:
   return ItineraryAttractionRecord(
      attraction=name,
      old_likelihood=None,
      new_likelihood=100 )


def _hyena_loop_pin() -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id=AFRICA_LOOP_ID,
      viewing_spot_index=HYENA_PIN_BOUNDARY,
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


def _grizzly_encounter_loop_pin() -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id=AFRICA_LOOP_ID,
      viewing_spot_index=GRIZZLY_ENCOUNTER_PIN_BOUNDARY,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
         item_key='Grizzly Bear',
         walk_node_ids=( 'v-0000', ),
         is_fixed_time=True,
         start_time='1:00 PM',
         end_time='1:45 PM' ),
      start_seconds=46800,
      end_seconds=49500,
   )


def _viewing_spot_index_for_stop(
      loop_id: str,
      stop: LoopScheduleStop.Stop,
      ) -> int | None:
   if isinstance( stop, ItineraryAnimalRecord ):
      return VIEWING_SPOT_INDEX_BY_ANIMAL.get(
         ( stop.species, stop.exhibit, stop.enclosure_name ) )

   if isinstance( stop, ItineraryAttractionRecord ):
      return VIEWING_SPOT_INDEX_BY_ATTRACTION.get( stop.attraction )

   return None


@pytest.fixture
def stub_viewing_spot_indexes( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'viewing_spot_index_for_stop',
      _viewing_spot_index_for_stop )


def Test_SegmentIndexForViewingSpot_TestBoundaries_ExpectBeforeAndAfterSegments() -> None:
   assert LoopPinSegmentSplitter.segment_index_for_viewing_spot(
      3,
      pin_boundaries=[ HYENA_PIN_BOUNDARY ] ) == 0
   assert LoopPinSegmentSplitter.segment_index_for_viewing_spot(
      HYENA_PIN_BOUNDARY,
      pin_boundaries=[ HYENA_PIN_BOUNDARY ] ) == 0
   assert LoopPinSegmentSplitter.segment_index_for_viewing_spot(
      20,
      pin_boundaries=[ HYENA_PIN_BOUNDARY ] ) == 1
   assert LoopPinSegmentSplitter.segment_index_for_viewing_spot(
      None,
      pin_boundaries=[ HYENA_PIN_BOUNDARY ] ) == 1


def Test_SplitStops_TestSavannaAnimals_ExpectPenguinBeforePin(
      stub_viewing_spot_indexes: None ) -> None:
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

   segments = LoopPinSegmentSplitter.split_stops(
      [ cheetah, penguin ],
      loop_id=AFRICA_LOOP_ID,
      loop_pins=[ loop_pin ],
   )

   assert [ animal.species for animal in segments[ 0 ] ] == [ 'African Penguin' ]
   assert [ animal.species for animal in segments[ 1 ] ] == [ 'Cheetah' ]


def Test_ScheduleSteps_TestSavannaAnimals_ExpectSegmentsAndGap(
      stub_viewing_spot_indexes: None ) -> None:
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

   steps = LoopPinSegmentSplitter.schedule_steps(
      [ penguin, cheetah ],
      loop_id=AFRICA_LOOP_ID,
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
   assert steps[ 0 ].end_before_seconds <= loop_pin.start_seconds
   assert loop_pin.start_seconds < loop_pin.end_seconds


def Test_SplitStops_TestWovenAttraction_ExpectPostPinAttractionAndAnimal(
      stub_viewing_spot_indexes: None ) -> None:
   kangaroo = _animal_record(
      species='Western Grey Kangaroo',
      exhibit='Australasia Outdoor',
   )
   walk_thru = _attraction_record( 'Kangaroo Walk-Thru' )
   tiger = _animal_record(
      species='Amur Tiger',
      exhibit='Eurasia Wilds',
   )
   loop_pin = LoopSchedulePin(
      loop_id=AUSTRALASIA_LOOP_ID,
      viewing_spot_index=KANGAROO_PIN_BOUNDARY,
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

   segments = LoopPinSegmentSplitter.split_stops(
      [ kangaroo, walk_thru, tiger ],
      loop_id=AUSTRALASIA_LOOP_ID,
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


def Test_SplitStops_TestGrizzlyEncounterPin_ExpectHyenaBeforeAndCheetahAfter(
      stub_viewing_spot_indexes: None ) -> None:
   loop_pin = _grizzly_encounter_loop_pin()
   hyena = _animal_record(
      species='Spotted Hyena',
      exhibit='Africa Savanna',
   )
   cheetah = _animal_record(
      species='Cheetah',
      exhibit='Africa Savanna',
   )

   segments = LoopPinSegmentSplitter.split_stops(
      [ hyena, cheetah ],
      loop_id=AFRICA_LOOP_ID,
      loop_pins=[ loop_pin ],
   )

   assert [ animal.species for animal in segments[ 0 ] ] == [ 'Spotted Hyena' ]
   assert [ animal.species for animal in segments[ 1 ] ] == [ 'Cheetah' ]


def Test_ScheduleSteps_TestGrizzlyEncounterPin_ExpectSegmentsAndGap(
      stub_viewing_spot_indexes: None ) -> None:
   loop_pin = _grizzly_encounter_loop_pin()
   hyena = _animal_record(
      species='Spotted Hyena',
      exhibit='Africa Savanna',
   )
   cheetah = _animal_record(
      species='Cheetah',
      exhibit='Africa Savanna',
   )
   window_end_seconds = 61200

   steps = LoopPinSegmentSplitter.schedule_steps(
      [ hyena, cheetah ],
      loop_id=AFRICA_LOOP_ID,
      loop_pins=[ loop_pin ],
      window_end_seconds=window_end_seconds,
   )

   assert len( steps ) == 3
   assert isinstance( steps[ 0 ], LoopPinStopSegment )
   assert [ animal.species for animal in steps[ 0 ].stops ] == [ 'Spotted Hyena' ]
   assert steps[ 0 ].end_before_seconds == loop_pin.start_seconds
   assert isinstance( steps[ 1 ], LoopPinGapStep )
   assert steps[ 1 ].loop_pin is loop_pin
   assert isinstance( steps[ 2 ], LoopPinStopSegment )
   assert [ animal.species for animal in steps[ 2 ].stops ] == [ 'Cheetah' ]
   assert steps[ 0 ].end_before_seconds <= loop_pin.start_seconds
   assert loop_pin.end_seconds < window_end_seconds
