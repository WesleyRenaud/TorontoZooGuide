from __future__ import annotations

from datetime import date
from pathlib import Path

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.attraction_hours import AttractionHours


class AttractionHoursFixer():
   @classmethod
   def apply(
         cls,
         database: Path,
         name: str,
         start: date,
         end: date | None,
         hours: AttractionHours ) -> bool:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         saved = AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
            name,
            start.isoformat(),
            None if end == None else end.isoformat(),
            hours.weekday_opens,
            hours.weekday_closes,
            hours.weekend_opens,
            hours.weekend_closes,
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      return saved
