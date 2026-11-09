from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from tools.checks.check_report import CheckReport


class WildEncounterInAppNotOnWebsiteFixer():
   @classmethod
   def fix( cls, database: Path, name: str ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         WildEncounterScheduleProvider.delete_schedules( connection, name )
         connection.commit()
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return CheckReport.detail_item( CheckReport.text( 'checks.removedSchedule' ) )
