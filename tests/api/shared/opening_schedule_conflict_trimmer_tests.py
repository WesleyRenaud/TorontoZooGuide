from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import cast

from api.shared.opening_schedule_conflict_delete_enclosed_trimmer import OpeningScheduleConflictDeleteEnclosedTrimmer
from api.shared.opening_schedule_conflict_shorten_end_trimmer import OpeningScheduleConflictShortenEndTrimmer
from api.shared.opening_schedule_conflict_shorten_start_trimmer import OpeningScheduleConflictShortenStartTrimmer
from api.shared.opening_schedule_conflict_split_wrap_trimmer import OpeningScheduleConflictSplitWrapTrimmer
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types


@dataclass
class SampleConflict():
   schedule_start_date: str
   schedule_end_date: str | None


@dataclass
class SampleSchedule():
   start_date: str
   end_date: str | None


STUB_CONNECTION = cast( Types.Connection, None )


def Test_DeleteEnclosedTrimmer_TestFullyEnclosedConflict_ExpectDeleteCalled() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-10',
      schedule_end_date='2026-06-20' )
   deleted: list[ SampleConflict ] = []

   trimmed = OpeningScheduleConflictDeleteEnclosedTrimmer.try_trim(
      STUB_CONNECTION,
      conflict,
      conflict_start_date=date( 2026, 6, 10 ),
      conflict_end_date=date( 2026, 6, 20 ),
      new_start_date=date( 2026, 6, 1 ),
      new_end_date=date( 2026, 6, 30 ),
      delete_conflict=lambda _conn, item: deleted.append( item ) )

   assert trimmed is True
   assert deleted == [ conflict ]


def Test_DeleteEnclosedTrimmer_TestPartialOverlap_ExpectNoTrim() -> None:
   trimmed = OpeningScheduleConflictDeleteEnclosedTrimmer.try_trim(
      STUB_CONNECTION,
      SampleConflict(
         schedule_start_date='2026-06-01',
         schedule_end_date='2026-06-30' ),
      conflict_start_date=date( 2026, 6, 1 ),
      conflict_end_date=date( 2026, 6, 30 ),
      new_start_date=date( 2026, 6, 10 ),
      new_end_date=date( 2026, 6, 20 ),
      delete_conflict=lambda _conn, _item: None )

   assert trimmed is False


def Test_ShortenEndTrimmer_TestOverlapAtStart_ExpectEndShortened() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-15' )
   updates: list[ tuple[ str | None, str | None ] ] = []

   trimmed = OpeningScheduleConflictShortenEndTrimmer.try_trim(
      STUB_CONNECTION,
      conflict,
      conflict_start_date=date( 2026, 6, 1 ),
      conflict_end_date=date( 2026, 6, 15 ),
      new_start_date=date( 2026, 6, 10 ),
      new_end_date=date( 2026, 6, 30 ),
      conflict_start_attr='schedule_start_date',
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ) )

   assert trimmed is True
   assert updates == [ ( '2026-06-01', '2026-06-09' ) ]


def Test_ShortenStartTrimmer_TestOverlapAtEnd_ExpectStartMovedForward() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-15',
      schedule_end_date='2026-06-30' )
   updates: list[ tuple[ str | None, str | None ] ] = []

   trimmed = OpeningScheduleConflictShortenStartTrimmer.try_trim(
      STUB_CONNECTION,
      conflict,
      conflict_start_date=date( 2026, 6, 15 ),
      conflict_end_date=date( 2026, 6, 30 ),
      new_start_date=date( 2026, 6, 1 ),
      new_end_date=date( 2026, 6, 20 ),
      conflict_end_attr='schedule_end_date',
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ) )

   assert trimmed is True
   assert updates == [ ( '2026-06-21', '2026-06-30' ) ]


def Test_SplitWrapTrimmer_TestConflictWrapsNewSchedule_ExpectSplitAroundNewRange() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30' )
   updates: list[ tuple[ str | None, str | None ] ] = []
   copies: list[ tuple[ str | None, str | None ] ] = []

   OpeningScheduleConflictSplitWrapTrimmer.trim(
      STUB_CONNECTION,
      conflict,
      new_start_date=date( 2026, 6, 10 ),
      new_end_date=date( 2026, 6, 20 ),
      conflict_start_attr='schedule_start_date',
      conflict_end_attr='schedule_end_date',
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ),
      insert_copy=lambda _conn, _item, start_date, end_date: copies.append(
         ( start_date, end_date ) ) )

   assert updates == [ ( '2026-06-01', '2026-06-09' ) ]
   assert copies == [ ( '2026-06-21', '2026-06-30' ) ]


def Test_ConflictTrimmer_TestEnclosedConflict_ExpectDeletePath() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-10',
      schedule_end_date='2026-06-20' )
   schedule = SampleSchedule(
      start_date='2026-06-01',
      end_date='2026-06-30' )
   deleted: list[ SampleConflict ] = []

   OpeningScheduleConflictTrimmer.trim(
      STUB_CONNECTION,
      conflict,
      schedule,
      delete_conflict=lambda _conn, item: deleted.append( item ),
      update_dates=lambda *_args: None,
      insert_copy=lambda *_args: None )

   assert deleted == [ conflict ]


def Test_ConflictTrimmer_TestOverlapAtStart_ExpectShortenEndPath() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-15' )
   schedule = SampleSchedule(
      start_date='2026-06-10',
      end_date='2026-06-30' )
   updates: list[ tuple[ str | None, str | None ] ] = []

   OpeningScheduleConflictTrimmer.trim(
      STUB_CONNECTION,
      conflict,
      schedule,
      delete_conflict=lambda _conn, _item: None,
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ),
      insert_copy=lambda *_args: None )

   assert updates == [ ( '2026-06-01', '2026-06-09' ) ]


def Test_ConflictTrimmer_TestOverlapAtEnd_ExpectShortenStartPath() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-15',
      schedule_end_date='2026-06-30' )
   schedule = SampleSchedule(
      start_date='2026-06-01',
      end_date='2026-06-20' )
   updates: list[ tuple[ str | None, str | None ] ] = []

   OpeningScheduleConflictTrimmer.trim(
      STUB_CONNECTION,
      conflict,
      schedule,
      delete_conflict=lambda _conn, _item: None,
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ),
      insert_copy=lambda *_args: None )

   assert updates == [ ( '2026-06-21', '2026-06-30' ) ]


def Test_ConflictTrimmer_TestConflictWrapsSchedule_ExpectSplitWrapPath() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30' )
   schedule = SampleSchedule(
      start_date='2026-06-10',
      end_date='2026-06-20' )
   updates: list[ tuple[ str | None, str | None ] ] = []
   copies: list[ tuple[ str | None, str | None ] ] = []

   OpeningScheduleConflictTrimmer.trim(
      STUB_CONNECTION,
      conflict,
      schedule,
      delete_conflict=lambda _conn, _item: None,
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ),
      insert_copy=lambda _conn, _item, start_date, end_date: copies.append(
         ( start_date, end_date ) ) )

   assert updates == [ ( '2026-06-01', '2026-06-09' ) ]
   assert copies == [ ( '2026-06-21', '2026-06-30' ) ]


def Test_SplitWrapTrimmer_TestOpenEndedNewSchedule_ExpectNoTrailingCopy() -> None:
   conflict = SampleConflict(
      schedule_start_date='2026-06-01',
      schedule_end_date='2026-06-30' )
   updates: list[ tuple[ str | None, str | None ] ] = []
   copies: list[ tuple[ str | None, str | None ] ] = []

   OpeningScheduleConflictSplitWrapTrimmer.trim(
      STUB_CONNECTION,
      conflict,
      new_start_date=date( 2026, 6, 10 ),
      new_end_date=date.max,
      conflict_start_attr='schedule_start_date',
      conflict_end_attr='schedule_end_date',
      update_dates=lambda _conn, _item, start_date, end_date: updates.append(
         ( start_date, end_date ) ),
      insert_copy=lambda _conn, _item, start_date, end_date: copies.append(
         ( start_date, end_date ) ) )

   assert updates == [ ( '2026-06-01', '2026-06-09' ) ]
   assert copies == []
