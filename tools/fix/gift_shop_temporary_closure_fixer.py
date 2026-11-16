from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.temporary_closure_change import TemporaryClosureChange
from tools.checks.temporary_closure_plan import TemporaryClosurePlan


class GiftShopTemporaryClosureFixer():
   @classmethod
   def save( cls, change: TemporaryClosureChange ) -> None:
      GiftShopCoordinator.set_gift_shop_closure_override(
         gift_shop=change.place,
         start_date=change.start,
         end_date=change.end,
         message=change.message,
      )


   @classmethod
   def apply( cls, database: Path, plan: TemporaryClosurePlan ) -> None:
      if plan.count() == 0:
         return

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         for change in plan.ended + plan.added + plan.extended:
            cls.save( change )
      finally:
         RequestConnectionProvider.clear()
         connection.close()

      CheckReport.note_fixed( plan.count() )
