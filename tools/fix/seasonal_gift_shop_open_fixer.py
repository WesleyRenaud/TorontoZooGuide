from __future__ import annotations

from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.request_connection_provider import RequestConnectionProvider
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.gift_shop_detail_image import GiftShopDetailImage
from tools.checks.paths import Paths


class SeasonalGiftShopOpenFixer():
   @classmethod
   def line( cls, name: str ) -> str:
      lines = [ ExhibitRegionColors.gift_shop_label( name ) ]
      photo = GiftShopDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         lines.append(
            CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo )
         )

      lines.append( CheckReport.detail_item( CheckReport.text( 'checks.setOpenForSeason' ) ) )
      return CheckReport.join_lines( lines )


   @classmethod
   def fix( cls, database: Path, names: list[ str ] ) -> list[ str ]:
      if names == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         lines = []

         for name in names:
            GiftShopCoordinator.set_gift_shop_as_open_for_season( name )
            lines.append( cls.line( name ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
