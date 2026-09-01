from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from api.models import WildEncounter
from api.shared.enums import ScheduleItemKind


ZEBRA_TALK = "Grevy's Zebra"
CAMEL_TALK = 'Bactrian Camel'
AFRICAN_LION_TALK = 'African Lion'
OTTER_TALK = 'North American River Otter'
BACTRIAN_CAMELS_ENCOUNTER = 'Bactrian Camels'
EURASIA_MEETING_SPOT = 'Wild Encounter - Eurasia Meeting Spot'


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


def _wild_encounter_stop( *, item_key: str ) -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key=item_key,
      walk_node_ids=( 'v-0100', ),
      meeting_spot=EURASIA_MEETING_SPOT,
      is_fixed_time=True,
      start_time='3:30 PM',
      end_time='4:00 PM' )


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


def Test_KeepCompletable_TestAdjacentCamelTalk_ExpectZebraPinDropped() -> None:
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
         end_seconds=12 * 3600,
         anchor_stop=ItineraryStop(
            schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
            item_key=ZEBRA_TALK,
            walk_node_ids=( 'v-0018', ),
            is_fixed_time=True,
            start_time='12:00 PM',
            end_time='12:30 PM' ) ),
      ItineraryScheduleWindow(
         start_seconds=13 * 3600,
         end_seconds=17 * 3600,
         opens_after_fixed_time_stop=True,
         start_walk_node_id='v-0044' ),
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


def Test_KeepCompletable_TestOtterTalk_ExpectKept() -> None:
   otter_pin = _talk_loop_pin(
      loop_id='americas_pavilion',
      viewing_spot_index=11,
      item_key=OTTER_TALK,
      start_seconds=14 * 3600,
      end_seconds=14 * 3600 + 30 * 60 )
   schedule_windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=14 * 3600 ),
      ItineraryScheduleWindow(
         start_seconds=14 * 3600 + 30 * 60,
         end_seconds=17 * 3600 ),
   ]

   kept_pins = BulkScheduleLoopPinAttacher.keep_completable(
      schedule_windows,
      [ otter_pin ] )

   assert kept_pins == [ otter_pin ]


def Test_AttachToWindows_TestAfricanLionTalk_ExpectPinOnBothWindows() -> None:
   lion_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=0,
      item_key=AFRICAN_LION_TALK,
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60 )
   schedule_windows = [
      ItineraryScheduleWindow(
         start_seconds=9 * 3600,
         end_seconds=11 * 3600 ),
      ItineraryScheduleWindow(
         start_seconds=11 * 3600 + 30 * 60,
         end_seconds=17 * 3600 ),
   ]

   attached_windows = BulkScheduleLoopPinAttacher.attach_to_windows(
      schedule_windows,
      [ lion_pin ] )

   assert len( attached_windows ) == 2
   assert attached_windows[ 0 ].start_seconds == 9 * 3600
   assert attached_windows[ 0 ].end_seconds == 11 * 3600
   assert attached_windows[ 1 ].start_seconds == 11 * 3600 + 30 * 60
   assert attached_windows[ 1 ].end_seconds == 17 * 3600
   assert len( attached_windows[ 0 ].loop_pins ) == 1
   assert len( attached_windows[ 1 ].loop_pins ) == 1
   assert attached_windows[ 0 ].loop_pins[ 0 ].stop.item_key == AFRICAN_LION_TALK


def Test_SeparateBoundariesAndPins_TestUnpinnedWildEncounter_ExpectNoLoopPin(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   encounter_stop = _wild_encounter_stop( item_key=BACTRIAN_CAMELS_ENCOUNTER )
   itinerary = ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[
         WildEncounter(
            name=BACTRIAN_CAMELS_ENCOUNTER,
            meeting_spot=EURASIA_MEETING_SPOT,
            link='https://example.com',
            x_coord=0.0,
            y_coord=0.0,
            start_time='3:30 PM',
            end_time='4:00 PM' ),
      ],
      events=[],
      arrival_time='9:30 AM',
      departure_time='12:00 PM' )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ encounter_stop ] )

   assert fixed_time_stops == [ encounter_stop ]
   assert loop_pins == []
