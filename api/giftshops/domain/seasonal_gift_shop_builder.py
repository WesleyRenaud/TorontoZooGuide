from __future__ import annotations

from ..data_access.gift_shop_closure_record import GiftShopClosureRecord
from .seasonal_gift_shop import SeasonalGiftShop
from ...shared.date_values import DateValues


class SeasonalGiftShopBuilder():
   @classmethod
   def build(
         cls,
         gift_shops: list[ str ],
         closure_records: list[ GiftShopClosureRecord ] ) -> list[ SeasonalGiftShop ]:
      closures = cls._closures( closure_records )
      return cls._listed( gift_shops, closures ) + cls._unlisted( gift_shops, closures )


   @classmethod
   def _closures(
         cls,
         closure_records: list[ GiftShopClosureRecord ] ) -> dict[ str, GiftShopClosureRecord ]:
      return {
         record.gift_shop: record
         for record in closure_records
         if record.closed_start != None
      }


   @classmethod
   def _listed(
         cls,
         gift_shops: list[ str ],
         closures: dict[ str, GiftShopClosureRecord ] ) -> list[ SeasonalGiftShop ]:
      return [
         cls._closure( name, closures[ name ] ) if name in closures else cls._open( name )
         for name in gift_shops
      ]


   @classmethod
   def _unlisted(
         cls,
         gift_shops: list[ str ],
         closures: dict[ str, GiftShopClosureRecord ] ) -> list[ SeasonalGiftShop ]:
      listed = set( gift_shops )
      return [
         cls._closure( name, record )
         for name, record in closures.items()
         if name not in listed
      ]


   @classmethod
   def _open( cls, name: str ) -> SeasonalGiftShop:
      return SeasonalGiftShop(
         name=name,
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      )


   @classmethod
   def _closure( cls, name: str, record: GiftShopClosureRecord ) -> SeasonalGiftShop:
      return SeasonalGiftShop(
         name=name,
         is_closed=True,
         start=DateValues.parse_date_value( record.closed_start ),
         end=DateValues.parse_date_value( record.closed_end ),
         closed_for_season=record.is_closed_for_season,
      )
