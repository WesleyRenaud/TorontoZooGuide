from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import cast

import pytest

from api.shared.opening_schedule_conflict_saver import OpeningScheduleConflictSaver
from api.shared.opening_schedule_conflict_trimmer import OpeningScheduleConflictTrimmer
from api.types import Types
from api.wild_encounters.data_access.wild_encounter_schedule_conflict_record import WildEncounterScheduleConflictRecord
from api.wild_encounters.data_access.wild_encounter_schedule_provider import WildEncounterScheduleProvider
from api.wild_encounters.scheduling.wild_encounter_schedule_conflict_resolver import WildEncounterScheduleConflictResolver
from api.wild_encounters.scheduling.wild_encounter_schedule_input import WildEncounterScheduleInput


WILD_ENCOUNTER_NAME = 'African Rainforest'
ENCOUNTER_TIME = '2:00 PM'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'June schedule.'


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


def _schedule_input( *, encounter_time: str = ENCOUNTER_TIME ) -> WildEncounterScheduleInput:
   return WildEncounterScheduleInput(
      wild_encounter=WILD_ENCOUNTER_NAME,
      start_date=START_DATE,
      end_date=END_DATE,
      encounter_time=encounter_time,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=MESSAGE )


def _conflict_record() -> WildEncounterScheduleConflictRecord:
   return WildEncounterScheduleConflictRecord(
      wild_encounter=WILD_ENCOUNTER_NAME,
      encounter_time=ENCOUNTER_TIME,
      schedule_start_date=START_DATE,
      schedule_end_date=END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=MESSAGE )


def Test_SaveReplacingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule_input()
   saver_calls: list[ tuple[ WildEncounterScheduleInput, Any ] ] = []

   def save_replacing_overlaps(
         _conn: Types.Connection,
         item: WildEncounterScheduleInput,
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

   assert WildEncounterScheduleConflictResolver.save_replacing_overlaps(
      STUB_CONNECTION,
      schedule ) is True
   assert saver_calls == [
      ( schedule, WildEncounterScheduleProvider.fetch_schedule_conflicts ),
   ]


def Test_SaveTrimmingOverlaps_TestSchedule_ExpectProviderBackedSaver(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   schedule = _schedule_input()
   saver_calls: list[ WildEncounterScheduleInput ] = []

   def save_trimming_overlaps(
         _conn: Types.Connection,
         item: WildEncounterScheduleInput,
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

   assert WildEncounterScheduleConflictResolver.save_trimming_overlaps(
      STUB_CONNECTION,
      schedule ) is True
   assert saver_calls == [ schedule ]


def Test_TrimConflict_TestConflictAndSchedule_ExpectTrimmerDelegation(
      monkeypatch: pytest.MonkeyPatch,
) -> None:
   conflict = _conflict_record()
   schedule = _schedule_input()
   trim_calls: list[ tuple[ WildEncounterScheduleConflictRecord, WildEncounterScheduleInput ] ] = []

   def trim(
         _conn: Types.Connection,
         item: WildEncounterScheduleConflictRecord,
         schedule_item: WildEncounterScheduleInput,
         *,
         delete_conflict: Any,
         update_dates: Any,
         insert_copy: Any,
   ) -> None:
      trim_calls.append( ( item, schedule_item ) )

   monkeypatch.setattr( OpeningScheduleConflictTrimmer, 'trim', trim )

   WildEncounterScheduleConflictResolver.trim_conflict(
      STUB_CONNECTION,
      conflict,
      schedule )

   assert trim_calls == [ ( conflict, schedule ) ]
