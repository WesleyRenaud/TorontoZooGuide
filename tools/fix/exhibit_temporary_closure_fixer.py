from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.temporary_closure_change import TemporaryClosureChange
from tools.checks.temporary_closure_plan import TemporaryClosurePlan


class ExhibitTemporaryClosureFixer():
   @classmethod
   def close( cls, change: TemporaryClosureChange ) -> None:
      ExhibitCoordinator.set_exhibit_as_closed(
         change.place,
         change.start,
         change.end,
         change.message,
         False,
      )


   @classmethod
   def open( cls, change: TemporaryClosureChange ) -> None:
      ExhibitCoordinator.set_exhibit_as_open(
         change.place,
         change.start,
         change.end,
      )


   @classmethod
   def apply( cls, database: Path, plan: TemporaryClosurePlan ) -> None:
      if plan.count() == 0:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         for change in plan.ended:
            cls.open( change )

         for change in plan.added + plan.extended:
            cls.close( change )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( plan.count() )
