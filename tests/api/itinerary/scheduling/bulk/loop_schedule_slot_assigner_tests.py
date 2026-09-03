from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.scheduling.bulk.loop_schedule_slot import LoopScheduleSlot
from api.itinerary.scheduling.bulk.loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.shared.calendar_dates import DateValues
from api.shared.operating_hours import OperatingHours
from api.types import Types

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


def _timed_stop(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None,
      duration_seconds: int = 0,
      travel_before_seconds: int = 0 ) -> TimedLoopScheduleStop:
   return TimedLoopScheduleStop(
      stop=_animal_record(
         species=species,
         exhibit=exhibit,
         enclosure_name=enclosure_name ),
      duration_seconds=duration_seconds,
      travel_before_seconds=travel_before_seconds,
   )


def _seconds( schedule_time: str | None ) -> int:
   value = DateValues.time_value_in_seconds( schedule_time )
   assert value is not None

   return value


def Test_AssignContiguous_TestInterStopTravel_ExpectGapsBetweenSlots() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=540 ),
   ]
   start_seconds = _seconds( '9:30 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   assert [ slot[ 1 ] for slot in slots ] == [ '9:30 AM', '9:44 AM' ]
   assert [ slot[ 2 ] for slot in slots ] == [ '9:35 AM', '9:52 AM' ]
   assert end_seconds == start_seconds + 300 + 540 + 480


def Test_AssignContiguous_TestNoTravel_ExpectFlushSlots() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=0 ),
   ]
   start_seconds = _seconds( '9:30 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   assert [ slot[ 1 ] for slot in slots ] == [ '9:30 AM', '9:35 AM' ]
   assert end_seconds == start_seconds + 300 + 480


def Test_AssignContiguous_TestZeroTravel_ExpectFlushBehavior() -> None:
   stops = [
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         duration_seconds=420,
         travel_before_seconds=0 ),
   ]
   start_seconds = _seconds( '10:00 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   assert slots[ 1 ][ 1 ] == '10:08 AM'
   assert end_seconds == start_seconds + 480 + 420


def Test_AssignContiguousEndingBy_TestDeadline_ExpectBackwardPackedSlots() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='African Lion',
         exhibit='Africa Savanna',
         duration_seconds=480,
         travel_before_seconds=540 ),
   ]
   deadline_seconds = _seconds( '11:00 AM' )
   assignment = LoopScheduleSlotAssigner.assign_contiguous_ending_by(
      stops,
      end_seconds=deadline_seconds )

   assert assignment is not None
   slots, end_seconds = assignment
   assert end_seconds == deadline_seconds
   assert slots[ 0 ][ 1 ] == '10:38 AM'
   assert slots[ 1 ][ 1 ] == '10:52 AM'


def Test_AssignContiguousRespectingAttractionHours_TestBeforeOpen_ExpectHeldUntilOpen() -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )
   stops = [
      TimedLoopScheduleStop(
         stop=splash,
         duration_seconds=60 * 60,
         travel_before_seconds=0 ),
   ]
   hours = OperatingHours(
      open_seconds=12 * 3600,
      close_seconds=17 * 3600 )

   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous_respecting_attraction_hours(
      stops,
      start_seconds=10 * 3600,
      hours_by_attraction_name={ 'Splash Island': hours } )

   assert slots == [ ( splash, '12:00 PM', '1:00 PM' ) ]
   assert end_seconds == 13 * 3600


def Test_AssignContiguousRespectingAttractionHours_TestCannotFit_ExpectEmpty() -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )
   stops = [
      TimedLoopScheduleStop(
         stop=splash,
         duration_seconds=60 * 60,
         travel_before_seconds=0 ),
   ]
   hours = OperatingHours(
      open_seconds=12 * 3600,
      close_seconds=12 * 3600 + 5 * 60 )

   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous_respecting_attraction_hours(
      stops,
      start_seconds=12 * 3600,
      hours_by_attraction_name={ 'Splash Island': hours } )

   assert slots == []
   assert end_seconds == 12 * 3600


def Test_AssignContiguous_TestWarthogBeforeGiraffe_ExpectEndBeforeStart() -> None:
   stops = [
      _timed_stop(
         species='Warthog',
         exhibit='Africa Savanna',
         duration_seconds=300,
         travel_before_seconds=0 ),
      _timed_stop(
         species='Masai Giraffe',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         duration_seconds=480,
         travel_before_seconds=120 ),
   ]
   start_seconds = _seconds( '11:30 AM' )
   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous(
      stops,
      start_seconds=start_seconds )

   warthog_end = _seconds( slots[ 0 ][ 2 ] )
   giraffe_start = _seconds( slots[ 1 ][ 1 ] )

   assert warthog_end <= giraffe_start


def Test_DurationSecondsForStop_TestStoredCustomTimes_ExpectElapsedSeconds() -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100,
      start_time='10:00 AM',
      end_time='10:20 AM',
   )

   duration_seconds = LoopScheduleSlotAssigner.duration_seconds_for_stop(
      sqlite3.connect( ':memory:' ),
      lion )

   assert duration_seconds == 20 * 60


def Test_DurationSecondsForStop_TestUnscheduledAnimal_ExpectDefaultDuration(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   lion = ItineraryAnimalRecord(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=None,
      new_likelihood=100,
   )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_assigner.ItineraryDefaultDurationProvider.fetch_enclosure_viewing_default_duration_seconds',
      lambda conn, species, exhibit, enclosure_name: 5 * 60 )

   duration_seconds = LoopScheduleSlotAssigner.duration_seconds_for_stop(
      sqlite3.connect( ':memory:' ),
      lion )

   assert duration_seconds == 5 * 60


def Test_PrepareStops_TestInterStopTravelAndDurations_ExpectTimedStops(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   first = _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' )
   second = _animal_record( species='African Lion', exhibit='Africa Savanna' )
   duration_by_stop = {
      id( first ): 300,
      id( second ): 480,
   }
   travel_by_stops = {
      id( first ): 0,
      id( second ): 540,
   }

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_assigner.LoopUnitTravelTimeCalculator.inter_stop_seconds',
      lambda walk_graph, stops, *, adjacency=None: [
         travel_by_stops[ id( stop ) ]
         for stop in stops
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'duration_seconds_for_stop',
      lambda conn, stop: duration_by_stop.get( id( stop ) ) )

   prepared = LoopScheduleSlotAssigner.prepare_stops(
      object(),
      object(),
      [ first, second ] )

   assert prepared is not None
   assert [ stop.duration_seconds for stop in prepared ] == [ 300, 480 ]
   assert [ stop.travel_before_seconds for stop in prepared ] == [ 0, 540 ]


def Test_PrepareStops_TestMissingDuration_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   animal = _animal_record( species='Cheetah', exhibit='Indo-Malaya Outdoor' )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_assigner.LoopUnitTravelTimeCalculator.inter_stop_seconds',
      lambda walk_graph, stops, *, adjacency=None: [ 0 ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'duration_seconds_for_stop',
      lambda conn, stop: None )

   assert LoopScheduleSlotAssigner.prepare_stops(
      object(),
      object(),
      [ animal ] ) is None


def Test_DefaultDurationSecondsForStop_TestAttraction_ExpectAttractionDefault(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_assigner.ItineraryDefaultDurationProvider.fetch_attraction_default_duration_seconds',
      lambda conn, attraction: 45 * 60 )

   assert LoopScheduleSlotAssigner.default_duration_seconds_for_stop(
      object(),
      splash ) == 45 * 60


def Test_DefaultDurationSecondsForStop_TestTransportation_ExpectTransportDefault(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   zoomobile = ItineraryTransportationRecord(
      transportation='Zoomobile',
      added_as_attraction=True,
      old_likelihood=None,
      new_likelihood=100 )

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_assigner.TransportationDefaultDurationResolver.resolve',
      lambda conn, transportation: 60 * 60 )

   assert LoopScheduleSlotAssigner.default_duration_seconds_for_stop(
      object(),
      zoomobile ) == 60 * 60


def Test_AssignContiguousRespectingAttractionHours_TestInvalidTimeKey_ExpectEmpty(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   splash = ItineraryAttractionRecord(
      attraction='Splash Island',
      old_likelihood=None,
      new_likelihood=100 )
   stops = [
      TimedLoopScheduleStop(
         stop=splash,
         duration_seconds=60 * 60,
         travel_before_seconds=0 ),
   ]

   monkeypatch.setattr(
      DateValues,
      'schedule_time_key_from_seconds',
      lambda seconds: None )

   slots, end_seconds = LoopScheduleSlotAssigner.assign_contiguous_respecting_attraction_hours(
      stops,
      start_seconds=10 * 3600,
      hours_by_attraction_name=None )

   assert slots == []
   assert end_seconds == 10 * 3600


def Test_AssignContiguousEndingBy_TestNegativeStart_ExpectNone() -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
   ]

   assert LoopScheduleSlotAssigner.assign_contiguous_ending_by(
      stops,
      end_seconds=0 ) is None


def Test_AssignContiguousEndingBy_TestSegmentOverflow_ExpectNone(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   stops = [
      _timed_stop(
         species='Cheetah',
         exhibit='Indo-Malaya Outdoor',
         duration_seconds=300,
         travel_before_seconds=0 ),
   ]

   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous',
      lambda stops, *, start_seconds: ( [], start_seconds + 400 ) )

   assert LoopScheduleSlotAssigner.assign_contiguous_ending_by(
      stops,
      end_seconds=300 ) is None


def Test_Save_TestDefaultSlotSink_ExpectDelegates(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved_calls: list[ object ] = []

   class _RecordingSink:
      def save(
            self,
            conn: Types.Connection,
            blockers: list[ TimeBlock ],
            stop_slots: list[ LoopScheduleSlot ] ) -> bool:
         saved_calls.append( ( conn, blockers, stop_slots ) )
         return True

   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.loop_schedule_slot_assigner.LoopScheduleSlotSink',
      _RecordingSink )

   result = LoopScheduleSlotAssigner.save(
      object(),
      [],
      [] )

   assert result is True
   assert len( saved_calls ) == 1
