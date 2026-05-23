from __future__ import annotations

from ... import zoo
from ...shared.enums.zoomobile_route import ZoomobileRouteId
from ...types import DateInput
from .zoomobile_current_route_schedule import ZoomobileCurrentRouteSchedule


def build_current_zoomobile_route_schedule(
      route: str,
      start_date: DateInput,
      end_date: DateInput ) -> ZoomobileCurrentRouteSchedule:
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   return ZoomobileCurrentRouteSchedule(
      route=ZoomobileRouteId( route ),
      start_date=date_range.start_date,
      end_date=date_range.end_date )
