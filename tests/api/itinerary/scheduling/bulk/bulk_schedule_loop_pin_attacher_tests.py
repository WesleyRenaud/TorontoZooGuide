from __future__ import annotations

import pytest

from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_schedule_window import ItineraryScheduleWindow
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher import BulkScheduleLoopPinAttacher
from api.models import GuardiansTalk
from api.models import Itinerary
from api.models import WildEncounter
from api.shared.calendar_dates import DateValues
from api.shared.enums import Position, ScheduleItemKind


ZEBRA_TALK = "Grevy's Zebra"
CAMEL_TALK = 'Bactrian Camel'
AFRICAN_LION_TALK = 'African Lion'
OTTER_TALK = 'North American River Otter'
BACTRIAN_CAMELS_ENCOUNTER = 'Bactrian Camels'
EURASIA_MEETING_SPOT = 'Wild Encounter - Eurasia Meeting Spot'

DAY_START_TIME = '9:00 AM'
DAY_END_TIME = '5:00 PM'
ARRIVAL_TIME = '9:30 AM'
NOON_TIME = '12:00 PM'
ZEBRA_START_TIME = NOON_TIME
ZEBRA_END_TIME = '12:30 PM'
CAMEL_START_TIME = ZEBRA_END_TIME
CAMEL_END_TIME = '1:00 PM'
LION_START_TIME = '11:00 AM'
LION_END_TIME = '11:30 AM'
OTTER_START_TIME = '2:00 PM'
OTTER_END_TIME = '2:30 PM'
ENCOUNTER_START_TIME = '3:30 PM'
ENCOUNTER_END_TIME = '4:00 PM'


def _seconds( schedule_time: str ) -> int:
   return DateValues.time_value_in_seconds( schedule_time )


def _talk_loop_pin(
      *,
      loop_id: str,
      viewing_spot_index: int,
      item_key: str,
      start_time: str,
      end_time: str ) -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id=loop_id,
      viewing_spot_index=viewing_spot_index,
      stop=ItineraryStop(
         schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
         item_key=item_key,
         walk_node_ids=( 'v-0000', ),
         is_fixed_time=True,
         start_time=start_time,
         end_time=end_time ),
      start_seconds=_seconds( start_time ),
      end_seconds=_seconds( end_time ),
   )


def _schedule_window(
      start_time: str,
      end_time: str,
      *,
      anchor_stop: ItineraryStop | None = None,
      opens_after_fixed_time_stop: bool = False,
      start_walk_node_id: str | None = None ) -> ItineraryScheduleWindow:
   return ItineraryScheduleWindow(
      start_seconds=_seconds( start_time ),
      end_seconds=_seconds( end_time ),
      anchor_stop=anchor_stop,
      opens_after_fixed_time_stop=opens_after_fixed_time_stop,
      start_walk_node_id=start_walk_node_id )


def _wild_encounter_stop( *, item_key: str ) -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key=item_key,
      walk_node_ids=( 'v-0100', ),
      meeting_spot=EURASIA_MEETING_SPOT,
      is_fixed_time=True,
      start_time=ENCOUNTER_START_TIME,
      end_time=ENCOUNTER_END_TIME )


def _lion_talk( *, is_deleted: bool = False ) -> GuardiansTalk:
   return GuardiansTalk(
      name=AFRICAN_LION_TALK,
      location='Africa Savanna',
      x_coord=0.0,
      y_coord=0.0,
      start_time=LION_START_TIME,
      end_time=LION_END_TIME,
      is_deleted=is_deleted )


def _camel_encounter( *, is_deleted: bool = False ) -> WildEncounter:
   return WildEncounter(
      name=BACTRIAN_CAMELS_ENCOUNTER,
      meeting_spot=EURASIA_MEETING_SPOT,
      link='https://example.com',
      x_coord=0.0,
      y_coord=0.0,
      start_time=ENCOUNTER_START_TIME,
      end_time=ENCOUNTER_END_TIME,
      is_deleted=is_deleted )


def _itinerary(
      *,
      arrival_time: str,
      departure_time: str,
      guardians_talks: list[ GuardiansTalk ] | None = None,
      wild_encounters: list[ WildEncounter ] | None = None ) -> Itinerary:
   return ItineraryBuilder.build(
      date='2026-06-20',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=guardians_talks or [],
      wild_encounters=wild_encounters or [],
      events=[],
      arrival_time=arrival_time,
      departure_time=departure_time )


def Test_KeepCompletable_TestPinWithoutPostTalkWindow_ExpectDropped() -> None:
   zebra_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=18,
      item_key=ZEBRA_TALK,
      start_time=ZEBRA_START_TIME,
      end_time=ZEBRA_END_TIME )
   camel_pin = _talk_loop_pin(
      loop_id='eurasia',
      viewing_spot_index=1,
      item_key=CAMEL_TALK,
      start_time=CAMEL_START_TIME,
      end_time=CAMEL_END_TIME )
   schedule_windows = [
      _schedule_window( DAY_START_TIME, ZEBRA_START_TIME ),
      _schedule_window( CAMEL_END_TIME, DAY_END_TIME ),
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
      start_time=ZEBRA_START_TIME,
      end_time=ZEBRA_END_TIME )
   camel_pin = _talk_loop_pin(
      loop_id='eurasia',
      viewing_spot_index=1,
      item_key=CAMEL_TALK,
      start_time=CAMEL_START_TIME,
      end_time=CAMEL_END_TIME )
   schedule_windows = [
      _schedule_window(
         DAY_START_TIME,
         ZEBRA_START_TIME,
         anchor_stop=ItineraryStop(
            schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
            item_key=ZEBRA_TALK,
            walk_node_ids=( 'v-0018', ),
            is_fixed_time=True,
            start_time=ZEBRA_START_TIME,
            end_time=ZEBRA_END_TIME ) ),
      _schedule_window(
         CAMEL_END_TIME,
         DAY_END_TIME,
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
      start_time=ZEBRA_START_TIME,
      end_time=ZEBRA_END_TIME )
   schedule_windows = [
      _schedule_window( DAY_START_TIME, ZEBRA_START_TIME ),
      _schedule_window( ZEBRA_END_TIME, DAY_END_TIME ),
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
      start_time=OTTER_START_TIME,
      end_time=OTTER_END_TIME )
   schedule_windows = [
      _schedule_window( DAY_START_TIME, OTTER_START_TIME ),
      _schedule_window( OTTER_END_TIME, DAY_END_TIME ),
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
      start_time=LION_START_TIME,
      end_time=LION_END_TIME )
   morning_window = _schedule_window( DAY_START_TIME, LION_START_TIME )
   afternoon_window = _schedule_window( LION_END_TIME, DAY_END_TIME )
   schedule_windows = [ morning_window, afternoon_window ]

   attached_windows = BulkScheduleLoopPinAttacher.attach_to_windows(
      schedule_windows,
      [ lion_pin ] )

   assert len( attached_windows ) == 2
   assert attached_windows[ Position.FIRST ].start_seconds == morning_window.start_seconds
   assert attached_windows[ Position.FIRST ].end_seconds == morning_window.end_seconds
   assert attached_windows[ Position.SECOND ].start_seconds == afternoon_window.start_seconds
   assert attached_windows[ Position.SECOND ].end_seconds == afternoon_window.end_seconds
   assert len( attached_windows[ Position.FIRST ].loop_pins ) == 1
   assert len( attached_windows[ Position.SECOND ].loop_pins ) == 1
   assert attached_windows[ Position.FIRST ].loop_pins[ Position.FIRST ].stop.item_key == AFRICAN_LION_TALK


def Test_SeparateBoundariesAndPins_TestUnpinnedWildEncounter_ExpectNoLoopPin(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   encounter_stop = _wild_encounter_stop( item_key=BACTRIAN_CAMELS_ENCOUNTER )
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=NOON_TIME,
      wild_encounters=[ _camel_encounter() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ encounter_stop ] )

   assert fixed_time_stops == [ encounter_stop ]
   assert loop_pins == []


def Test_SeparateBoundariesAndPins_TestGuardiansTalkPinned_ExpectLoopPin(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   talk_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key=AFRICAN_LION_TALK,
      walk_node_ids=( 'v-0000', ),
      is_fixed_time=True,
      start_time=LION_START_TIME,
      end_time=LION_END_TIME )
   expected_pin = _talk_loop_pin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=0,
      item_key=AFRICAN_LION_TALK,
      start_time=LION_START_TIME,
      end_time=LION_END_TIME )
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      guardians_talks=[ _lion_talk() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.GuardiansTalkLoopSchedulePinResolver.resolve',
      lambda conn, talk, fixed_time_stop: expected_pin )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ talk_stop ] )

   assert fixed_time_stops == [ talk_stop ]
   assert loop_pins == [ expected_pin ]


def Test_SeparateBoundariesAndPins_TestDeletedGuardiansTalk_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   talk_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key=AFRICAN_LION_TALK,
      walk_node_ids=( 'v-0000', ),
      is_fixed_time=True,
      start_time=LION_START_TIME,
      end_time=LION_END_TIME )
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      guardians_talks=[ _lion_talk( is_deleted=True ) ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ talk_stop ] )

   assert fixed_time_stops == [ talk_stop ]
   assert loop_pins == []


def Test_SeparateBoundariesAndPins_TestWildEncounterPinned_ExpectLoopPin(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   encounter_stop = _wild_encounter_stop( item_key=BACTRIAN_CAMELS_ENCOUNTER )
   expected_pin = LoopSchedulePin(
      loop_id='eurasia',
      viewing_spot_index=1,
      stop=encounter_stop,
      start_seconds=_seconds( encounter_stop.start_time ),
      end_seconds=_seconds( encounter_stop.end_time ) )
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      wild_encounters=[ _camel_encounter() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: { EURASIA_MEETING_SPOT: object() } )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterLoopSchedulePinResolver.resolve',
      lambda wild_encounter, fixed_time_stop, *, meeting_spot_loop_pins_by_name: expected_pin )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ encounter_stop ] )

   assert fixed_time_stops == [ encounter_stop ]
   assert loop_pins == [ expected_pin ]


def Test_SeparateBoundariesAndPins_TestDeletedWildEncounter_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   encounter_stop = _wild_encounter_stop( item_key=BACTRIAN_CAMELS_ENCOUNTER )
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      wild_encounters=[ _camel_encounter( is_deleted=True ) ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ encounter_stop ] )

   assert fixed_time_stops == [ encounter_stop ]
   assert loop_pins == []


def Test_SeparateBoundariesAndPins_TestGuardiansTalkWithoutFixedStop_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      guardians_talks=[ _lion_talk() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [] )

   assert fixed_time_stops == []
   assert loop_pins == []


def Test_SeparateBoundariesAndPins_TestGuardiansTalkResolveNone_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   talk_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key=AFRICAN_LION_TALK,
      walk_node_ids=( 'v-0000', ),
      is_fixed_time=True,
      start_time=LION_START_TIME,
      end_time=LION_END_TIME )
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      guardians_talks=[ _lion_talk() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.GuardiansTalkLoopSchedulePinResolver.resolve',
      lambda conn, talk, fixed_time_stop: None )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [ talk_stop ] )

   assert fixed_time_stops == [ talk_stop ]
   assert loop_pins == []


def Test_SeparateBoundariesAndPins_TestWildEncounterWithoutFixedStop_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   itinerary = _itinerary(
      arrival_time=ARRIVAL_TIME,
      departure_time=DAY_END_TIME,
      wild_encounters=[ _camel_encounter() ] )
   monkeypatch.setattr(
      'api.itinerary.scheduling.bulk.bulk_schedule_loop_pin_attacher.WildEncounterMeetingSpotLoopPinProvider.fetch_meeting_spot_loop_pins_by_name',
      lambda conn: {} )

   fixed_time_stops, loop_pins = BulkScheduleLoopPinAttacher.separate_boundaries_and_pins(
      None,
      itinerary,
      [] )

   assert fixed_time_stops == []
   assert loop_pins == []


def Test_AttachToWindows_TestEmptyLoopPins_ExpectSameWindows() -> None:
   schedule_windows = [
      _schedule_window( DAY_START_TIME, NOON_TIME ),
   ]

   result = BulkScheduleLoopPinAttacher.attach_to_windows(
      schedule_windows,
      [] )

   assert result is schedule_windows
