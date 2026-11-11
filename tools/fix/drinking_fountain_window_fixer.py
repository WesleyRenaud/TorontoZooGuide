from __future__ import annotations

from pathlib import Path

from api.app_string_provider import AppStringProvider
from api.database_connection_provider import DatabaseConnectionProvider
from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.drinking_fountain_window import DrinkingFountainWindow


class DrinkingFountainWindowFixer():
   @classmethod
   def line( cls, window: DrinkingFountainWindow ) -> str:
      return CheckReport.join_lines( [
         AppStringProvider.format( 'checks.countNames.drinkingFountains' ),
         window.detail(),
      ] )


   @classmethod
   def apply( cls, database: Path, window: DrinkingFountainWindow ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         DrinkingFountainCoordinator.set_drinking_fountain_window(
            window.closed,
            window.start,
            window.end,
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return cls.line( window )
