from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.loop_pin_gap_step import LoopPinGapStep
from api.itinerary.scheduling.bulk.loop_pin_segment_splitter import LoopPinSegmentSplitter
from api.itinerary.scheduling.bulk.loop_pin_stop_segment import LoopPinStopSegment
from api.itinerary.scheduling.bulk.loop_schedule_slot import LoopScheduleSlot
from api.itinerary.scheduling.bulk.loop_schedule_slot_assigner import LoopScheduleSlotAssigner
from api.itinerary.scheduling.bulk.loop_schedule_slot_sink import LoopScheduleSlotSink
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_unit_pin_scheduler import LoopUnitPinScheduler
from api.itinerary.scheduling.bulk.loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.itinerary.scheduling.bulk.timed_loop_schedule_stop import TimedLoopScheduleStop
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider

LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)

CHEETAH = ItineraryAnimalRecord(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
   old_likelihood=None,
   new_likelihood=100,
)

LOOP_ID = 'africa_savanna'

PIN_START_SECONDS = 12 * 3600
PIN_END_SECONDS = 12 * 3600 + 30 * 60
ANIMAL_DURATION_SECONDS = 30 * 60
WINDOW_START_SECONDS = 9 * 3600
WINDOW_END_SECONDS = 17 * 3600
CURSOR_SECONDS = 10 * 3600


def _raise_persist_error() -> None:
   raise LoopUnitSchedulePersistError( [ CHEETAH ] )


def _pin(
      *,
      loop_id: str,
      start_seconds: int,
      end_seconds: int | None = None ) -> LoopSchedulePin:
   return LoopSchedulePin(
      loop_id=loop_id,
      viewing_spot_index=0,
      stop=ItineraryStop(
         walk_node_ids=[ 'n-lion' ],
         schedule_item_kind=ScheduleItemKind.ANIMAL,
         item_key='African Lion||Africa Savanna' ),
      start_seconds=start_seconds,
      end_seconds=end_seconds or start_seconds + 30 * 60 )


def _prepared_unit(
      *,
      loop_id: str | None,
      stops: list[ ItineraryAnimalRecord ] ) -> PreparedLoopScheduleUnit:
   return PreparedLoopScheduleUnit(
      unit=LoopScheduleUnit(
         loop_id=loop_id,
         stops=stops,
         entry_walk_node_id='n-entry',
         exit_walk_node_id='n-exit',
         side_cluster_id=None,
         loop_index_in_side_cluster=None,
         traversal=None ),
      occupied_seconds=0 )


def _timed_stop(
      stop: ItineraryAnimalRecord,
      *,
      duration_seconds: int = ANIMAL_DURATION_SECONDS,
   ) -> TimedLoopScheduleStop:
   return TimedLoopScheduleStop(
      stop=stop,
      duration_seconds=duration_seconds,
      travel_before_seconds=0 )


def _raise_on_schedule( *_args: object, **_kwargs: object ) -> None:
   _raise_persist_error()


@pytest.fixture
def pin_scheduler_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_PinsForUnit_TestMixedLoopIds_ExpectSortedUnitPins() -> None:
   pins = [
      _pin( loop_id=LOOP_ID, start_seconds=11 * 3600 ),
      _pin( loop_id='other-loop', start_seconds=9 * 3600 ),
      _pin( loop_id=LOOP_ID, start_seconds=10 * 3600 ),
   ]

   unit_pins = LoopUnitPinScheduler.pins_for_unit( LOOP_ID, pins )

   assert [ pin.start_seconds for pin in unit_pins ] == [ 10 * 3600, 11 * 3600 ]


def Test_Schedule_TestNoLoopId_ExpectStopsAndCursorUnchanged(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   prepared_unit = _prepared_unit( loop_id=None, stops=[ LION, CHEETAH ] )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestNoPinsForUnit_ExpectStopsAndCursorUnchanged(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ _pin( loop_id='other-loop', start_seconds=10 * 3600 ) ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestPersistError_ExpectErrorStopsReturned(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )

   monkeypatch.setattr(
      LoopUnitPinScheduler,
      '_schedule_animals_around_loop_pins',
      _raise_on_schedule )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ _pin( loop_id=LOOP_ID, start_seconds=10 * 3600 ) ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_EarliestStartSeconds_TestNoLoopId_ExpectNone(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   assert LoopUnitPinScheduler.earliest_start_seconds(
      pin_scheduler_conn,
      _prepared_unit( loop_id=None, stops=[ LION ] ),
      [ _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS ) ] ) is None


def Test_EarliestStartSeconds_TestNoUnitPins_ExpectNone(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   assert LoopUnitPinScheduler.earliest_start_seconds(
      pin_scheduler_conn,
      _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] ),
      [ _pin( loop_id='other-loop', start_seconds=PIN_START_SECONDS ) ] ) is None


def Test_EarliestStartSeconds_TestNoAnimalsBeforePin_ExpectPinStart(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'animals_before_first_pin',
      lambda *_args, **_kwargs: [] )

   assert LoopUnitPinScheduler.earliest_start_seconds(
      pin_scheduler_conn,
      _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] ),
      [ _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS ) ]
   ) == PIN_START_SECONDS


def Test_EarliestStartSeconds_TestPrepareStopsFails_ExpectNone(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'animals_before_first_pin',
      lambda *_args, **_kwargs: [ LION ] )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: None )

   assert LoopUnitPinScheduler.earliest_start_seconds(
      pin_scheduler_conn,
      _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] ),
      [ _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS ) ] ) is None


def Test_EarliestStartSeconds_TestAnimalsBeforePin_ExpectPinMinusOccupied(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'animals_before_first_pin',
      lambda *_args, **_kwargs: [ LION, CHEETAH ] )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [
         _timed_stop( LION, duration_seconds=20 * 60 ),
         _timed_stop( CHEETAH, duration_seconds=10 * 60 ),
      ] )

   assert LoopUnitPinScheduler.earliest_start_seconds(
      pin_scheduler_conn,
      _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] ),
      [ _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS ) ]
   ) == PIN_START_SECONDS - 30 * 60


def Test_Schedule_TestAroundPinsHappyPath_ExpectAnimalsScheduledAndCursorAtPinEnd(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )
   slot_sink = LoopScheduleSlotSink( persist=False )
   saved_slots: list[ LoopScheduleSlot ] = []

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=PIN_START_SECONDS,
            anchor_at_end=True ),
         LoopPinGapStep( loop_pin=unit_pin ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: sum(
         timed_stop.occupied_seconds() for timed_stop in prepared_stops ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_ending_by',
      lambda prepared_stops, *, end_seconds: (
         [
            LoopScheduleSlot( LION, '11:30 AM', '12:00 PM' ),
         ],
         end_seconds,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, animal_slots, *, slot_sink=None: (
         saved_slots.extend( animal_slots ) or True ) )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS,
      slot_sink=slot_sink )

   assert still_unscheduled == []
   assert cursor_seconds == PIN_END_SECONDS
   assert saved_slots == [ LoopScheduleSlot( LION, '11:30 AM', '12:00 PM' ) ]


def Test_Schedule_TestPrepareStopsFailure_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=PIN_START_SECONDS,
            anchor_at_end=True ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: None )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestWindowOverrun_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )
   past_window_cursor = WINDOW_END_SECONDS + 60

   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [] )
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=past_window_cursor )

   assert still_unscheduled == [ LION ]
   assert cursor_seconds == past_window_cursor


def Test_Schedule_TestGapAlreadyPassed_ExpectSkipGapAndScheduleForward(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )
   saved_slots: list[ LoopScheduleSlot ] = []

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinGapStep( loop_pin=unit_pin ),
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=WINDOW_END_SECONDS,
            anchor_at_end=False ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous',
      lambda prepared_stops, *, start_seconds: (
         [ LoopScheduleSlot( LION, '12:30 PM', '1:00 PM' ) ],
         start_seconds + ANIMAL_DURATION_SECONDS,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, animal_slots, *, slot_sink=None: (
         saved_slots.extend( animal_slots ) or True ) )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=PIN_END_SECONDS )

   assert still_unscheduled == []
   assert cursor_seconds == PIN_END_SECONDS + ANIMAL_DURATION_SECONDS
   assert saved_slots == [ LoopScheduleSlot( LION, '12:30 PM', '1:00 PM' ) ]


def Test_Schedule_TestPinPastWindow_ExpectUnscheduledReturned(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=WINDOW_END_SECONDS + 60,
      end_seconds=WINDOW_END_SECONDS + 30 * 60 )

   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [ LoopPinGapStep( loop_pin=unit_pin ) ] )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestSkipBeforePinSegment_ExpectRemainingForward(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )
   saved_slots: list[ LoopScheduleSlot ] = []

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=PIN_START_SECONDS,
            anchor_at_end=False ),
         LoopPinGapStep( loop_pin=unit_pin ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous',
      lambda prepared_stops, *, start_seconds: (
         [ LoopScheduleSlot( LION, '12:30 PM', '1:00 PM' ) ],
         start_seconds + ANIMAL_DURATION_SECONDS,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, animal_slots, *, slot_sink=None: (
         saved_slots.extend( animal_slots ) or True ) )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == []
   assert cursor_seconds == PIN_END_SECONDS + ANIMAL_DURATION_SECONDS
   assert saved_slots == [ LoopScheduleSlot( LION, '12:30 PM', '1:00 PM' ) ]


def Test_Schedule_TestForwardDoesNotFit_ExpectUnscheduledKept(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [ LoopPinGapStep( loop_pin=unit_pin ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION, duration_seconds=8 * 3600 ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 8 * 3600 )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION ]
   assert cursor_seconds == PIN_END_SECONDS


def Test_Schedule_TestBackwardAnchorTooTight_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=PIN_START_SECONDS,
            anchor_at_end=True ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION, duration_seconds=3 * 3600 ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 3 * 3600 )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestForwardAssignEmptySlots_ExpectCursorUnchanged(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [ LoopPinGapStep( loop_pin=unit_pin ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous',
      lambda prepared_stops, *, start_seconds: ( [], start_seconds ) )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION ]
   assert cursor_seconds == PIN_END_SECONDS


def Test_Schedule_TestForwardSaveFails_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [ LoopPinGapStep( loop_pin=unit_pin ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous',
      lambda prepared_stops, *, start_seconds: (
         [ LoopScheduleSlot( LION, '12:30 PM', '1:00 PM' ) ],
         start_seconds + ANIMAL_DURATION_SECONDS,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, animal_slots, *, slot_sink=None: False )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_ShouldSkipAnimalSegmentStep_TestNoPinsForward_ExpectFalse() -> None:
   assert not LoopUnitPinScheduler._should_skip_animal_segment_step(
      LoopPinStopSegment(
         stops=[ LION ],
         end_before_seconds=PIN_START_SECONDS,
         anchor_at_end=False ),
      loop_pins=[],
      schedule_cursor_seconds=CURSOR_SECONDS )


def Test_ScheduleAnimalSegmentStep_TestAlreadyScheduledStops_ExpectCursorUnchanged(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   scheduled_animal_ids = { id( LION ) }

   cursor = LoopUnitPinScheduler._schedule_animal_segment_step(
      pin_scheduler_conn,
      LoopPinStopSegment(
         stops=[ LION ],
         end_before_seconds=PIN_START_SECONDS,
         anchor_at_end=True ),
      blockers=[],
      animals=[ LION ],
      loop_pins=[ _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS ) ],
      schedule_cursor_seconds=CURSOR_SECONDS,
      scheduled_animal_ids=scheduled_animal_ids )

   assert cursor == CURSOR_SECONDS


def Test_Schedule_TestForwardStartAtSegmentEnd_ExpectPersistError(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=CURSOR_SECONDS,
            anchor_at_end=False ),
      ] )
   monkeypatch.setattr(
      LoopUnitPinScheduler,
      '_should_skip_animal_segment_step',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestRemainingPrepareFails_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [ LoopPinGapStep( loop_pin=unit_pin ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: None )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_ScheduleAnimalsAroundLoopPins_TestNoneLoopId_ExpectPersistError(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   with pytest.raises( LoopUnitSchedulePersistError ) as raised:
      LoopUnitPinScheduler._schedule_animals_around_loop_pins(
         pin_scheduler_conn,
         _prepared_unit( loop_id=None, stops=[ LION ] ),
         [ _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS ) ],
         blockers=[],
         window_start_seconds=WINDOW_START_SECONDS,
         window_end_seconds=WINDOW_END_SECONDS,
         cursor_seconds=CURSOR_SECONDS )

   assert raised.value.stops == [ LION ]


def Test_Schedule_TestForwardSegmentTooLarge_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=CURSOR_SECONDS + 15 * 60,
            anchor_at_end=False ),
      ] )
   monkeypatch.setattr(
      LoopUnitPinScheduler,
      '_should_skip_animal_segment_step',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION, duration_seconds=30 * 60 ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 30 * 60 )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestBackwardEmptySlots_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=PIN_START_SECONDS,
            anchor_at_end=True ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_ending_by',
      lambda prepared_stops, *, end_seconds: ( [], end_seconds ) )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestSegmentSaveFails_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin(
      loop_id=LOOP_ID,
      start_seconds=PIN_START_SECONDS,
      end_seconds=PIN_END_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=WINDOW_END_SECONDS,
            anchor_at_end=False ),
      ] )
   monkeypatch.setattr(
      LoopUnitPinScheduler,
      '_should_skip_animal_segment_step',
      lambda *_args, **_kwargs: False )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous',
      lambda prepared_stops, *, start_seconds: (
         [ LoopScheduleSlot( LION, '12:30 PM', '1:00 PM' ) ],
         start_seconds + ANIMAL_DURATION_SECONDS,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, animal_slots, *, slot_sink=None: False )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_Schedule_TestBackwardAssignNone_ExpectPersistErrorStops(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION, CHEETAH ] )
   unit_pin = _pin( loop_id=LOOP_ID, start_seconds=PIN_START_SECONDS )

   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopPinSegmentSplitter,
      'schedule_steps',
      lambda *_args, **_kwargs: [
         LoopPinStopSegment(
            stops=[ LION ],
            end_before_seconds=PIN_START_SECONDS,
            anchor_at_end=True ),
      ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: ANIMAL_DURATION_SECONDS )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_ending_by',
      lambda prepared_stops, *, end_seconds: None )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ unit_pin ],
      blockers=[],
      window_start_seconds=WINDOW_START_SECONDS,
      window_end_seconds=WINDOW_END_SECONDS,
      cursor_seconds=CURSOR_SECONDS )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == CURSOR_SECONDS


def Test_ScheduleAnimalSegment_TestEffectiveStartBeforeWindow_ExpectPersistError(
      pin_scheduler_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( WalkGraphProvider, 'fetch', lambda: {} )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'prepare_stops',
      lambda *_args, **_kwargs: [ _timed_stop( LION ) ] )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'total_occupied_seconds',
      lambda prepared_stops: 200 )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'assign_contiguous_ending_by',
      lambda prepared_stops, *, end_seconds: (
         [ LoopScheduleSlot( stop=LION, start_seconds=500, end_seconds=700 ) ],
         700,
      ) )
   monkeypatch.setattr(
      LoopScheduleSlotAssigner,
      'save',
      lambda conn, blockers, stop_slots, *, slot_sink=None: True )

   with pytest.raises( LoopUnitSchedulePersistError ) as raised:
      LoopUnitPinScheduler._schedule_animal_segment(
         pin_scheduler_conn,
         blockers=[],
         animals=[ LION ],
         animal_group=[ LION ],
         start_seconds=600,
         segment_end_seconds=700,
         backward_anchor=True )

   assert raised.value.stops == [ LION ]
