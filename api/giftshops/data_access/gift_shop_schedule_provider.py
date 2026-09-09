from __future__ import annotations

from .gift_shop_schedule_mapper import GiftShopScheduleMapper
from .gift_shop_schedule_record import GiftShopScheduleRecord
from ..scheduling.gift_shop_opening_schedule import GiftShopOpeningSchedule
from ..scheduling.gift_shop_schedule_override import GiftShopScheduleOverride
from ...shared.amenity_opening_schedule_provider import AmenityOpeningScheduleProvider
from ...shared.enums import AmenityNameField
from ...types import Types


class GiftShopScheduleProvider():
   _provider = AmenityOpeningScheduleProvider(
      name_field=AmenityNameField.GIFT_SHOP,
      opening_table='GiftShopOpeningSchedule',
      override_table='GiftShopScheduleOverride',
      map_records=GiftShopScheduleMapper.map_records,
   )


   @classmethod
   def overlaps_existing_schedule(
         cls,
         conn: Types.Connection,
         schedule: GiftShopOpeningSchedule ) -> bool:
      return cls._provider.overlaps_existing_schedule( conn, schedule )


   @classmethod
   def save_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: GiftShopOpeningSchedule ) -> bool:
      if cls.overlaps_existing_schedule( conn, schedule ):
         return False

      cls.insert_or_update_opening_schedule( conn, schedule )
      conn.commit()
      return True


   @classmethod
   def fetch_opening_schedule_conflicts(
         cls,
         conn: Types.Connection,
         schedule: GiftShopOpeningSchedule ) -> list[ GiftShopScheduleRecord ]:
      return cls._provider.fetch_opening_schedule_conflicts( conn, schedule )


   @classmethod
   def delete_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: GiftShopScheduleRecord ) -> None:
      cls._provider.delete_opening_schedule( conn, schedule )


   @classmethod
   def update_opening_schedule_dates(
         cls,
         conn: Types.Connection,
         schedule: GiftShopScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cls._provider.update_opening_schedule_dates( conn, schedule, start_date, end_date )


   @classmethod
   def insert_copied_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: GiftShopScheduleRecord,
         start_date: Types.DateKey,
         end_date: Types.DateKey | None ) -> None:
      cls._provider.insert_copied_opening_schedule( conn, schedule, start_date, end_date )


   @classmethod
   def insert_or_update_opening_schedule(
         cls,
         conn: Types.Connection,
         schedule: GiftShopOpeningSchedule ) -> None:
      cls._provider.insert_or_update_opening_schedule( conn, schedule )


   @classmethod
   def save_schedule_override(
         cls,
         conn: Types.Connection,
         override: GiftShopScheduleOverride ) -> bool:
      return cls._provider.save_schedule_override( conn, override )
