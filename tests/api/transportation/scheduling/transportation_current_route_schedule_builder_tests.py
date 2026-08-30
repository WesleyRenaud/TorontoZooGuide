from __future__ import annotations

from api.transportation.scheduling.transportation_current_route_schedule_builder import TransportationCurrentRouteScheduleBuilder


ROUTE_NAME = 'summer'
START_DATE = '2026-06-01'
END_DATE = '2026-09-30'


def Test_BuildCurrentTransportationRouteSchedule_TestDateRange_ExpectMappedSchedule() -> None:
   schedule = TransportationCurrentRouteScheduleBuilder.build_current_transportation_route_schedule(
      route=ROUTE_NAME,
      start_date=START_DATE,
      end_date=END_DATE )

   assert schedule.route == ROUTE_NAME
   assert schedule.start_date == START_DATE
   assert schedule.end_date == END_DATE


def Test_BuildCurrentTransportationRouteSchedule_TestOpenEndedRange_ExpectNullEndDate() -> None:
   schedule = TransportationCurrentRouteScheduleBuilder.build_current_transportation_route_schedule(
      route=ROUTE_NAME,
      start_date=START_DATE,
      end_date=None )

   assert schedule.start_date == START_DATE
   assert schedule.end_date is None
