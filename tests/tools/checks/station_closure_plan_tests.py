from __future__ import annotations

from datetime import date

from api.transportation.data_access.transportation_station_status_record import TransportationStationStatusRecord
from tools.checks.station_closure import StationClosure
from tools.checks.station_closure_plan import StationClosurePlan


TODAY = date( 2026, 11, 14 )
EURASIA = 'Eurasia Zoomobile Station'
TUNDRA = 'Tundra Zoomobile Station'
MESSAGE = 'The Eurasia Zoomobile stop is closed at this time.'
SRT = (
   'The Scarborough Rapid Transit (SRT) car at the Tundra Zoomobile Station '
   'will be closed for a private event.'
)


def record(
      station: str,
      is_closed: int,
      message: str,
      start: str,
      end: str | None ) -> TransportationStationStatusRecord:
   return TransportationStationStatusRecord(
      station,
      start,
      end,
      bool( is_closed ),
      message,
   )


def Test_Build_TestUndatedNotice_ExpectTwoWeeks() -> None:
   plan = StationClosurePlan.build(
      [ StationClosure( EURASIA, MESSAGE, None, None ) ],
      [],
      TODAY,
   )

   assert [ ( change.station, change.start, change.end ) for change in plan.added ] == [
      ( EURASIA, TODAY, date( 2026, 11, 28 ) ),
   ]
   assert plan.ended == []
   assert plan.extended == []


def Test_Build_TestDatedNotice_ExpectPageRange() -> None:
   plan = StationClosurePlan.build(
      [ StationClosure( TUNDRA, SRT, date( 2026, 4, 20 ), date( 2026, 4, 22 ) ) ],
      [],
      date( 2026, 4, 21 ),
   )

   assert [ ( change.start, change.end ) for change in plan.added ] == [
      ( date( 2026, 4, 20 ), date( 2026, 4, 22 ) ),
   ]


def Test_Build_TestMissingNotice_ExpectEnded() -> None:
   plan = StationClosurePlan.build(
      [],
      [ record( EURASIA, 1, MESSAGE, '2026-11-01', '2026-12-01' ) ],
      TODAY,
   )

   assert [ change.station for change in plan.ended ] == [ EURASIA ]
   assert plan.added == []
   assert plan.extended == []


def Test_Build_TestSoonerEnd_ExpectExtended() -> None:
   plan = StationClosurePlan.build(
      [ StationClosure( EURASIA, MESSAGE, None, None ) ],
      [ record( EURASIA, 1, MESSAGE, '2026-11-01', '2026-11-20' ) ],
      TODAY,
   )

   assert [ ( change.start, change.end ) for change in plan.extended ] == [
      ( date( 2026, 11, 1 ), date( 2026, 11, 28 ) ),
   ]
   assert plan.added == []
   assert plan.ended == []


def Test_Build_TestLaterEnd_ExpectLeftAlone() -> None:
   plan = StationClosurePlan.build(
      [ StationClosure( EURASIA, MESSAGE, None, None ) ],
      [ record( EURASIA, 1, MESSAGE, '2026-11-01', '2026-12-01' ) ],
      TODAY,
   )

   assert plan.added == []
   assert plan.ended == []
   assert plan.extended == []


def Test_Build_TestDifferentRange_ExpectRealigned() -> None:
   plan = StationClosurePlan.build(
      [ StationClosure( TUNDRA, SRT, date( 2026, 4, 20 ), date( 2026, 4, 22 ) ) ],
      [ record( TUNDRA, 1, SRT, '2026-04-20', '2026-04-30' ) ],
      date( 2026, 4, 21 ),
   )

   assert [ ( change.start, change.end ) for change in plan.extended ] == [
      ( date( 2026, 4, 20 ), date( 2026, 4, 22 ) ),
   ]
   assert plan.added == []
   assert plan.ended == []


def Test_Build_TestPastRow_ExpectLeftAlone() -> None:
   plan = StationClosurePlan.build(
      [],
      [ record( TUNDRA, 1, SRT, '2026-04-23', '2026-04-30' ) ],
      TODAY,
   )

   assert plan.added == []
   assert plan.ended == []
   assert plan.extended == []


def Test_Build_TestOpenEndedRowMissing_ExpectEnded() -> None:
   plan = StationClosurePlan.build(
      [],
      [ record( EURASIA, 1, MESSAGE, '2026-11-01', None ) ],
      TODAY,
   )

   assert [ change.station for change in plan.ended ] == [ EURASIA ]
   assert plan.added == []


def Test_Build_TestOpenEndedRow_ExpectLeftAlone() -> None:
   plan = StationClosurePlan.build(
      [ StationClosure( EURASIA, MESSAGE, None, None ) ],
      [ record( EURASIA, 1, MESSAGE, '2026-11-01', None ) ],
      TODAY,
   )

   assert plan.added == []
   assert plan.ended == []
   assert plan.extended == []


def Test_Build_TestChangedMessage_ExpectEndedAndAdded() -> None:
   replacement = 'The Eurasia Zoomobile station is closed for maintenance.'
   plan = StationClosurePlan.build(
      [ StationClosure( EURASIA, replacement, None, None ) ],
      [ record( EURASIA, 1, MESSAGE, '2026-11-01', '2026-12-01' ) ],
      TODAY,
   )

   assert [ change.message for change in plan.ended ] == [ MESSAGE ]
   assert [ ( change.message, change.start, change.end ) for change in plan.added ] == [
      ( replacement, TODAY, date( 2026, 11, 28 ) ),
   ]
