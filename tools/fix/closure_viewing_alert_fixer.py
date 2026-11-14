from __future__ import annotations

from pathlib import Path

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.animals.status.animal_viewing_alert import AnimalViewingAlert
from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.closure_viewing_alert import ClosureViewingAlert


class ClosureViewingAlertFixer():
   @classmethod
   def save( cls, alerts: list[ ClosureViewingAlert ] ) -> list[ ClosureViewingAlert ]:
      for alert in alerts:
         wrote = AnimalCoordinator.set_animal_viewing_alert(
            species=alert.species,
            exhibit=alert.exhibit,
            alert_start_date=alert.start,
            alert_end_date=alert.end,
            message=alert.message,
         )

         if not wrote:
            raise RuntimeError(
               AppStringProvider.format( 'checks.couldNotWriteViewingAlert' )
            )

      return alerts


   @classmethod
   def remove( cls, alerts: list[ AnimalViewingAlert ] ) -> list[ AnimalViewingAlert ]:
      removed = []

      for alert in alerts:
         deleted = AnimalCoordinator.remove_animal_viewing_alert(
            alert.species,
            alert.exhibit,
         )

         if deleted:
            removed.append( alert )

      return removed


   @classmethod
   def apply(
         cls,
         database: Path,
         alerts: list[ ClosureViewingAlert ],
         removals: list[ AnimalViewingAlert ] ) -> tuple[
            list[ ClosureViewingAlert ],
            list[ AnimalViewingAlert ] ]:
      if len( alerts ) == 0 and len( removals ) == 0:
         return [], []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         saved = cls.save( alerts )
         removed = cls.remove( removals )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      changed = len( saved ) + len( removed )

      if changed > 0:
         CheckReport.note_fixed( changed )

      return saved, removed
