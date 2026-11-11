from __future__ import annotations

from datetime import date
from pathlib import Path

from api.database_connection_provider import DatabaseConnectionProvider
from api.giftshops.coordinators.gift_shop_coordinator import GiftShopCoordinator
from api.giftshops.domain.seasonal_gift_shop import SeasonalGiftShop
from api.request_connection_provider import RequestConnectionProvider
from api.shared.date_values import DateValues
from tools.checks.check_report import CheckReport
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.gift_shop_detail_image import GiftShopDetailImage
from tools.checks.paths import Paths
from tools.checks.season_window import SeasonWindow


class SeasonalGiftShopClosedWeekFixer():
   @classmethod
   def extension_end( cls, gift_shop: SeasonalGiftShop, today: date ) -> date:
      return SeasonWindow.week_extension_end( gift_shop.end, today )


   @classmethod
   def item( cls, name: str, detail: str ) -> str:
      lines = [ ExhibitRegionColors.gift_shop_label( name ) ]
      photo = GiftShopDetailImage.source( name )

      if ( Paths.ROOT / photo ).is_file():
         lines.append(
            CheckReport.detail_item( CheckReport.text( 'checks.photo' ) + photo )
         )

      lines.append( CheckReport.detail_item( detail ) )
      return CheckReport.join_lines( lines )


   @classmethod
   def line( cls, name: str, end: date ) -> str:
      return cls.item(
         name,
         CheckReport.text( 'checks.extendedClosedForSeasonThrough' )
         + DateValues.format_display_date_value( end )
         + CheckReport.text( 'checks.period' ),
      )


   @classmethod
   def fix( cls, database: Path, today: date, names: list[ str ] ) -> list[ str ]:
      if names == []:
         return []

      connection = DatabaseConnectionProvider.open( str( database ) )
      RequestConnectionProvider.set( connection )

      try:
         gift_shops = {
            gift_shop.name: gift_shop
            for gift_shop in GiftShopCoordinator.get_seasonal_gift_shops()
         }
         lines = []

         for name in names:
            gift_shop = gift_shops[ name ]
            start = today if gift_shop.start == None else gift_shop.start
            end = cls.extension_end( gift_shop, today )
            GiftShopCoordinator.set_gift_shop_as_closed_for_season(
               gift_shop=name,
               start_date=start,
               end_date=end,
               message='',
            )
            lines.append( cls.line( name, end ) )

         CheckReport.note_fixed( len( lines ) )
         return lines
      finally:
         RequestConnectionProvider.clear()
         connection.close()
