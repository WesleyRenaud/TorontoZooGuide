from __future__ import annotations

from ..data_access.gift_shop_schedule_provider import GiftShopScheduleProvider
from ..data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from .gift_shop_opening_schedule import GiftShopOpeningSchedule
from ...shared.opening_schedule_conflict_resolution import OpeningScheduleConflictResolution
from ...types import Types


_resolution = OpeningScheduleConflictResolution(
   fetch_conflicts=GiftShopScheduleProvider.fetch_opening_schedule_conflicts,
   delete_conflict=GiftShopScheduleProvider.delete_opening_schedule,
   insert_or_update=GiftShopScheduleProvider.insert_or_update_opening_schedule,
   update_dates=GiftShopScheduleProvider.update_opening_schedule_dates,
   insert_copy=GiftShopScheduleProvider.insert_copied_opening_schedule,
)


class GiftShopScheduleConflictResolver():
   @classmethod
   def save_replacing_overlaps(
         cls,
         conn: Types.Connection,
         schedule: GiftShopOpeningSchedule ) -> bool:
      return _resolution.save_replacing_overlaps( conn, schedule )


   @classmethod
   def save_trimming_overlaps(
         cls,
         conn: Types.Connection,
         schedule: GiftShopOpeningSchedule ) -> bool:
      return _resolution.save_trimming_overlaps( conn, schedule )


   @classmethod
   def trim_conflict(
         cls,
         conn: Types.Connection,
         conflict: GiftShopScheduleRecord,
         schedule: GiftShopOpeningSchedule ) -> None:
      return _resolution.trim_conflict( conn, conflict, schedule )
