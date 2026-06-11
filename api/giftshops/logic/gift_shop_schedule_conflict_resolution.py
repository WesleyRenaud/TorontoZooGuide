from __future__ import annotations

from ..data_access.gift_shop_schedule import delete_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import fetch_gift_shop_opening_schedule_conflicts
from ..data_access.gift_shop_schedule import insert_copied_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import insert_or_update_gift_shop_opening_schedule
from ..data_access.gift_shop_schedule import update_gift_shop_opening_schedule_dates
from ..data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from .gift_shop_opening_schedule import GiftShopOpeningSchedule
from ...shared.opening_schedule_conflict import save_opening_schedule_replacing_overlaps
from ...shared.opening_schedule_conflict import save_opening_schedule_trimming_overlaps
from ...shared.opening_schedule_conflict import trim_opening_schedule_conflict
from ...types import Connection


def save_gift_shop_opening_schedule_replacing_overlaps(
      conn: Connection,
      schedule: GiftShopOpeningSchedule ) -> bool:
   return save_opening_schedule_replacing_overlaps(
      conn,
      schedule,
      fetch_conflicts=fetch_gift_shop_opening_schedule_conflicts,
      delete_conflict=delete_gift_shop_opening_schedule,
      insert_or_update=insert_or_update_gift_shop_opening_schedule )


def save_gift_shop_opening_schedule_trimming_overlaps(
      conn: Connection,
      schedule: GiftShopOpeningSchedule ) -> bool:
   return save_opening_schedule_trimming_overlaps(
      conn,
      schedule,
      fetch_conflicts=fetch_gift_shop_opening_schedule_conflicts,
      trim_conflict=trim_gift_shop_opening_schedule_conflict,
      insert_or_update=insert_or_update_gift_shop_opening_schedule )


def trim_gift_shop_opening_schedule_conflict(
      conn: Connection,
      conflict: GiftShopScheduleRecord,
      schedule: GiftShopOpeningSchedule ) -> None:
   trim_opening_schedule_conflict(
      conn,
      conflict,
      schedule,
      delete_conflict=delete_gift_shop_opening_schedule,
      update_dates=update_gift_shop_opening_schedule_dates,
      insert_copy=insert_copied_gift_shop_opening_schedule )


__all__ = [
   'save_gift_shop_opening_schedule_replacing_overlaps',
   'save_gift_shop_opening_schedule_trimming_overlaps',
   'trim_gift_shop_opening_schedule_conflict',
]
