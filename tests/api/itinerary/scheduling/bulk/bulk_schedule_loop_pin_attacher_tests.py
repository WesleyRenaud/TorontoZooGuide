from __future__ import annotations

from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from api.shared.enums import ScheduleItemKind


ZEBRA_TALK = "Grevy's Zebra"
CAMEL_TALK = 'Bactrian Camel'


def _talk_loop_pin(
      *,
      loop_id: str,
      viewing_spot_index: int,
      item_key: str,
      start_seconds: int,
      end_seconds: int ) -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id=loop_id,
      viewing_spot_index=viewing_spot_index,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key=item_key,
         walk_node_ids=( 'v-0000', ),
         is_fixed_time=True ),
      start_seconds=start_seconds,
      end_seconds=end_seconds,
   )


def Test_KeepCompletable_TestPinWithoutPostTalkWindow_ExpectDropped() -> None:
   zebra_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=18,
      item_key=ZEBRA_TALK,
      start_seconds=12 * 3600,
      end_seconds=12 * 3600 + 30 * 60 )
   camel_pin = _talk_loop_pin(
      loop_id='eurasia',
      viewing_spot_index=1,
      item_key=CAMEL_TALK,
      start_seconds=12 * 3600 + 30 * 60,
      end_seconds=13 * 3600 )
   schedule_windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=12 * 3600 ),
      ItineraryScheduleWindow(
         start_seconds=13 * 3600,
         end_seconds=17 * 3600 ),
   ]

   kept_pins = BulkScheduleLoopPinAttacher.keep_completable(
      schedule_windows,
      [ zebra_pin, camel_pin ] )

   assert kept_pins == [ camel_pin ]


def Test_KeepCompletable_TestPinWithPostTalkWindow_ExpectKept() -> None:
   zebra_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=18,
      item_key=ZEBRA_TALK,
      start_seconds=12 * 3600,
      end_seconds=12 * 3600 + 30 * 60 )
   schedule_windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=12 * 3600 ),
      ItineraryScheduleWindow(
         start_seconds=12 * 3600 + 30 * 60,
         end_seconds=17 * 3600 ),
   ]

   kept_pins = BulkScheduleLoopPinAttacher.keep_completable(
      schedule_windows,
      [ zebra_pin ] )

   assert kept_pins == [ zebra_pin ]
