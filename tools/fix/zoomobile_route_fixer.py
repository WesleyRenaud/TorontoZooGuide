from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from tools.checks.check_report import CheckReport
from tools.checks.zoomobile_route_change import ZoomobileRouteChange
from tools.checks.zoomobile_route_plan import ZoomobileRoutePlan


class ZoomobileRouteFixer():
   @classmethod
   def save( cls, writes: list[ ZoomobileRouteChange ] ) -> None:
      for change in writes:
         TransportationCoordinator.set_current_transportation_route(
            route=change.route,
            start_date=change.start,
            end_date=change.end,
         )


   @classmethod
   def apply( cls, database: Path, plan: ZoomobileRoutePlan ) -> None:
      if plan.count() == 0:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         cls.save( plan.writes )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
