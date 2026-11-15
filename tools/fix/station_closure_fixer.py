from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from tools.checks.check_report import CheckReport
from tools.checks.station_change import StationChange
from tools.checks.station_closure_plan import StationClosurePlan


class StationClosureFixer():
   @classmethod
   def add( cls, additions: list[ StationChange ] ) -> None:
      for change in additions:
         TransportationCoordinator.set_transportation_station_as_closed(
            transportation_station=change.station,
            start_date=change.start,
            end_date=change.end,
            message=change.message,
         )


   @classmethod
   def clear( cls, endings: list[ StationChange ] ) -> None:
      for change in endings:
         TransportationCoordinator.set_transportation_station_as_open(
            transportation_station=change.station,
         )


   @classmethod
   def extend( cls, extensions: list[ StationChange ] ) -> None:
      cls.add( extensions )


   @classmethod
   def apply( cls, database: Path, plan: StationClosurePlan ) -> None:
      if plan.count() == 0:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         cls.clear( plan.ended )
         cls.add( plan.added )
         cls.extend( plan.extended )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( plan.count() )
