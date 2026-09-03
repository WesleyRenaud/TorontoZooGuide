from __future__ import annotations

from typing import Any

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.giftshops.data_access.gift_shop_schedule_provider import GiftShopScheduleProvider
from api.giftshops.data_access.gift_shop_schedule_record import GiftShopScheduleRecord
from api.giftshops.scheduling.gift_shop_opening_schedule import GiftShopOpeningSchedule
from api.giftshops.scheduling.gift_shop_schedule_conflict_resolver import GiftShopScheduleConflictResolver
from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types

GIFT_SHOP = 'Zootique'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Summer hours.'


def _schedule() -> GiftShopOpeningSchedule:
   return GiftShopOpeningSchedule(
      gift_shop=GIFT_SHOP,
      start_date=START_DATE,
      end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=MESSAGE )


def _conflict_record() -> GiftShopScheduleRecord:
   return GiftShopScheduleRecord(
      gift_shop=GIFT_SHOP,
      schedule_start_date=START_DATE,
      schedule_end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      schedule_message=MESSAGE )


def Test_SaveReplacingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule()
   saver_calls: list[ tuple[ GiftShopOpeningSchedule, Any ] ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         item: GiftShopOpeningSchedule,
         *,
         fetch_conflicts: Any,
         delete_conflict: Any,
         insert_or_update: Any,
   ) -> bool:
      saver_calls.append( ( item, fetch_conflicts ) )
      return True

   monkeypatch.setattr(
      OpeningScheduleConflictSaver,
      'save_replacing_overlaps',
      save_replacing_overlaps )

   assert GiftShopScheduleConflictResolver.save_replacing_overlaps(
      STUB_REQUEST_CONNECTION,
      schedule ) is True
   assert saver_calls == [
      ( schedule, GiftShopScheduleProvider.fetch_opening_schedule_conflicts ),
   ]


def Test_SaveTrimmingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule()
   saver_calls: list[ GiftShopOpeningSchedule ] = []

   def save_trimming_overlaps(
         _conn: Types.Connection,
         item: GiftShopOpeningSchedule,
         *,
         fetch_conflicts: Any,
         trim_conflict: Any,
         insert_or_update: Any,
   ) -> bool:
      saver_calls.append( item )
      return True

   monkeypatch.setattr(
      OpeningScheduleConflictSaver,
      'save_trimming_overlaps',
      save_trimming_overlaps )

   assert GiftShopScheduleConflictResolver.save_trimming_overlaps(
      STUB_REQUEST_CONNECTION,
      schedule ) is True
   assert saver_calls == [ schedule ]


def Test_TrimConflict_TestConflictAndSchedule_ExpectTrimmerDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   conflict = _conflict_record()
   schedule = _schedule()
   trim_calls: list[ tuple[ GiftShopScheduleRecord, GiftShopOpeningSchedule ] ] = []

   def trim(
         _conn: Types.Connection,
         item: GiftShopScheduleRecord,
         schedule_item: GiftShopOpeningSchedule,
         *,
         delete_conflict: Any,
         update_dates: Any,
         insert_copy: Any,
   ) -> None:
      trim_calls.append( ( item, schedule_item ) )

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   GiftShopScheduleConflictResolver.trim_conflict(
      STUB_REQUEST_CONNECTION,
      conflict,
      schedule )

   assert trim_calls == [ ( conflict, schedule ) ]
