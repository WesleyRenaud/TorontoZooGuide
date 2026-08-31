from __future__ import annotations

from api.itinerary.domain.itinerary_visit_window_builder import ItineraryVisitWindowBuilder


def Test_ScheduleTimeOccursOutside_TestBeforeArrival_ExpectTrue() -> None:
   assert ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      '9:00 AM',
      '9:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )


def Test_ScheduleTimeOccursOutside_TestAfterDeparture_ExpectTrue() -> None:
   assert ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      '4:30 PM',
      '5:30 PM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )


def Test_ScheduleTimeOccursOutside_TestInsideWindow_ExpectFalse() -> None:
   assert not ItineraryVisitWindowBuilder.schedule_time_occurs_outside(
      '11:00 AM',
      '11:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' )


def Test_ClearedScheduleTimes_TestOutsideWindow_ExpectCleared() -> None:
   assert ItineraryVisitWindowBuilder.cleared_schedule_times(
      '9:00 AM',
      '9:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' ) == ( None, None )


def Test_ClearedScheduleTimes_TestInsideWindow_ExpectUnchanged() -> None:
   assert ItineraryVisitWindowBuilder.cleared_schedule_times(
      '11:00 AM',
      '11:30 AM',
      arrival_time='10:00 AM',
      departure_time='5:00 PM' ) == ( '11:00 AM', '11:30 AM' )
