from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.opening_window import OpeningWindow


class GiftShopWindowFixer():
   @classmethod
   def apply( cls, database: Path, name: str, window: OpeningWindow ) -> str:
      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         monday, tuesday, wednesday, thursday, friday, saturday, sunday = (
            window.pattern.weekday_values()
         )
         GiftShopCoordinator.replace_gift_shop_opening_schedule_overlaps(
            name,
            window.start.isoformat(),
            window.stored_end(),
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
            window.pattern.holidays_only,
            '',
         )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( 1 )
      return OpeningWindow.detail( window )
