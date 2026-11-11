from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.models import ZooHours
from api.request_connection_provider import RequestConnectionProvider
from api.zoo_hours.coordinators.zoo_hours_coordinator import ZooHoursCoordinator
from tools.checks.check_report import CheckReport


class ZooHoursFixer():
   @classmethod
   def apply(
         cls,
         database: Path,
         saved: list[ ZooHours ],
         removed: list[ ZooHours ] ) -> None:
      if not saved and not removed:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         for hours in saved:
            ZooHoursCoordinator.set_zoo_hours( hours )

         for hours in removed:
            ZooHoursCoordinator.delete_zoo_hours( hours.date )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( len( saved ) + len( removed ) )
