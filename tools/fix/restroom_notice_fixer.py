from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from tools.checks.check_report import CheckReport
from tools.checks.restroom_change import RestroomChange
from tools.checks.restroom_notice_plan import RestroomNoticePlan


class RestroomNoticeFixer():
   @classmethod
   def add( cls, additions: list[ RestroomChange ] ) -> None:
      for change in additions:
         if change.closure:
            RestroomCoordinator.set_restroom_as_closed(
               restroom=change.restroom,
               start_date=change.start,
               end_date=change.end,
               message=change.message,
            )
            continue

         RestroomCoordinator.set_restroom_alert(
            restroom=change.restroom,
            alert_start_date=change.start,
            alert_end_date=change.end,
            message=change.message,
         )


   @classmethod
   def clear( cls, endings: list[ RestroomChange ] ) -> None:
      for change in endings:
         if change.closure:
            RestroomCoordinator.set_restroom_as_open(
               restroom=change.restroom,
               start_date=change.start,
               end_date=change.end,
            )
            continue

         RestroomCoordinator.remove_restroom_alert( restroom=change.restroom )


   @classmethod
   def extend( cls, extensions: list[ RestroomChange ] ) -> None:
      cls.add( extensions )


   @classmethod
   def apply( cls, database: Path, plan: RestroomNoticePlan ) -> None:
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
