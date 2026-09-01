from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.scheduling.bulk.loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.shared.calendar_dates import DateValues
from api.shared.operating_hours import OperatingHours


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
