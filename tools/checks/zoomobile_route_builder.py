from __future__ import annotations

from datetime import date

from api.shared.calendar_dates import CalendarDates
from api.shared.date_values import DateValues
from api.shared.enums.transportation_route_id import TransportationRouteId
from api.transportation.scheduling.transportation_current_route_schedule import TransportationCurrentRouteSchedule
from api.transportation.scheduling.zoomobile_season import ZoomobileSeason
from .zoomobile_route_change import ZoomobileRouteChange
from .zoomobile_route_plan import ZoomobileRoutePlan


class ZoomobileRouteBuilder():
   @classmethod
   def through( cls, route: str, today: date ) -> date:
      if cls.aligns( route, today ):
         return cls.window_end( route, today )

      return CalendarDates.two_weeks_later( today )


   @classmethod
   def aligns( cls, route: str, today: date ) -> bool:
      if route == TransportationRouteId.SUMMER.value:
         return today.month == 4 or today.month in ZoomobileSeason.SUMMER_MONTHS

      return today.month == 10 or today.month in ZoomobileSeason.WINTER_MONTHS


   @classmethod
   def window_end( cls, route: str, today: date ) -> date:
      if route == TransportationRouteId.SUMMER.value:
         return date( today.year, 10, 31 )

      year = today.year + 1 if today.month >= 10 else today.year
      return date( year, 4, 30 )


   @classmethod
   def on_day( cls, value: str | date | None ) -> date | None:
      if value in ( None, '' ):
         return None

      return DateValues.parse_date_value( value )


   @classmethod
   def covers( cls, schedule: TransportationCurrentRouteSchedule, today: date ) -> bool:
      start = cls.on_day( schedule.start_date )

      if start == None:
         return False

      return DateValues.is_date_in_range( today, start, cls.on_day( schedule.end_date ) )


   @classmethod
   def covering(
         cls,
         schedules: list[ TransportationCurrentRouteSchedule ],
         today: date ) -> TransportationCurrentRouteSchedule | None:
      active = [
         schedule
         for schedule in schedules
         if cls.covers( schedule, today )
      ]

      if active == []:
         return None

      return max( active, key=lambda schedule: schedule.start_date )


   @classmethod
   def change_for(
         cls,
         route: str,
         current: TransportationCurrentRouteSchedule | None,
         today: date,
         end: date ) -> ZoomobileRouteChange:
      if current == None or current.route != route:
         return ZoomobileRouteChange( route, today, end )

      start = cls.on_day( current.start_date )
      return ZoomobileRouteChange( route, start, end )


   @classmethod
   def scheduled(
         cls,
         current: TransportationCurrentRouteSchedule | None,
         route: str,
         end: date ) -> bool:
      if current == None:
         return False

      return current.route == route and cls.on_day( current.end_date ) == end


   @classmethod
   def earlier_route(
         cls,
         schedule: TransportationCurrentRouteSchedule,
         target_start: date ) -> bool:
      start = cls.on_day( schedule.start_date )
      return start != None and start < target_start


   @classmethod
   def runs_past(
         cls,
         schedule: TransportationCurrentRouteSchedule,
         last_day: date ) -> bool:
      end = cls.on_day( schedule.end_date )
      return end == None or end > last_day


   @classmethod
   def trimmed(
         cls,
         schedules: list[ TransportationCurrentRouteSchedule ],
         target_start: date ) -> list[ ZoomobileRouteChange ]:
      last_day = CalendarDates.one_day_earlier( target_start )
      return [
         ZoomobileRouteChange( schedule.route, cls.on_day( schedule.start_date ), last_day )
         for schedule in schedules
         if cls.earlier_route( schedule, target_start )
         if cls.runs_past( schedule, last_day )
      ]


   @classmethod
   def build(
         cls,
         route: str,
         schedules: list[ TransportationCurrentRouteSchedule ],
         today: date ) -> ZoomobileRoutePlan:
      end = cls.through( route, today )
      current = cls.covering( schedules, today )

      if cls.scheduled( current, route, end ):
         return ZoomobileRoutePlan( [], None, False )

      change = cls.change_for( route, current, today, end )
      rows = cls.trimmed( schedules, change.start )
      rows.append( change )
      return ZoomobileRoutePlan( rows, change, current == None )
