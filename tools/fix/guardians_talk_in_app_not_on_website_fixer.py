from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.guardians.data_access.guardians_talk_schedule_provider import GuardiansTalkScheduleProvider
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport


class GuardiansTalkInAppNotOnWebsiteFixer():
   @classmethod
   def fix( cls, database: Path, name: str, location: str ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         GuardiansTalkScheduleProvider.delete_schedules( connection, name, location )
         connection.commit()
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return CheckReport.detail_item( CheckReport.text( 'checks.removedSchedule' ) )
