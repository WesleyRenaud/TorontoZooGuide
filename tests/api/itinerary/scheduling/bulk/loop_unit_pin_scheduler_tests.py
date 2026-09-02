from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.loop_schedule_unit import LoopScheduleUnit
from api.itinerary.scheduling.bulk.loop_unit_pin_scheduler import LoopUnitPinScheduler
from api.itinerary.scheduling.bulk.loop_unit_schedule_persist_error import LoopUnitSchedulePersistError
from api.itinerary.scheduling.bulk.prepared_loop_schedule_unit import PreparedLoopScheduleUnit
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.shared.enums import ScheduleItemKind


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
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600 )

   assert still_unscheduled == [ LION, CHEETAH ]
   assert cursor_seconds == 10 * 3600


def Test_Schedule_TestNoPinsForUnit_ExpectStopsAndCursorUnchanged(
      pin_scheduler_conn: sqlite3.Connection ) -> None:
   prepared_unit = _prepared_unit( loop_id=LOOP_ID, stops=[ LION ] )

   still_unscheduled, cursor_seconds = LoopUnitPinScheduler.schedule(
      pin_scheduler_conn,
      prepared_unit,
      [ _pin( loop_id='other-loop', start_seconds=10 * 3600 ) ],
      blockers=[],
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600 )

   assert still_unscheduled == [ LION ]
   assert cursor_seconds == 10 * 3600


def _raise_on_schedule( *_args: object, **_kwargs: object ) -> None:
   _raise_persist_error()


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
      window_start_seconds=9 * 3600,
      window_end_seconds=17 * 3600,
      cursor_seconds=10 * 3600 )

   assert still_unscheduled == [ CHEETAH ]
   assert cursor_seconds == 10 * 3600
