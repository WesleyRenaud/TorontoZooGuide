from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import pytest

from api.request_connection_provider import RequestConnectionProvider
from api.restaurants.scheduling.restaurant_opening_schedule import RestaurantOpeningSchedule
from api.restaurants.scheduling.restaurant_schedule_override import RestaurantScheduleOverride
from api.shared.amenity_coordinator_mutations import AmenityCoordinatorMutations
from api.types import Types


AMENITY_NAME = 'Africa Restaurant'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for testing.'


@dataclass
class StubConnection():
   pass


STUB_CONNECTION = cast( Types.Connection, StubConnection() )


def _mutations(
      *,
      saved_schedules: list[ RestaurantOpeningSchedule ],
      saved_overrides: list[ RestaurantScheduleOverride ],
      replaced: list[ RestaurantOpeningSchedule ],
      trimmed: list[ RestaurantOpeningSchedule ],
) -> AmenityCoordinatorMutations[ RestaurantOpeningSchedule, RestaurantScheduleOverride ]:
   return AmenityCoordinatorMutations(
      build_closed_schedule=lambda name, start_date, end_date, message: RestaurantOpeningSchedule(
         restaurant=name,
         start_date=start_date,
         end_date=end_date,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=False,
         sunday=False,
         holidays_only=False,
         message=message ),
      build_opening_schedule=lambda name, start_date, end_date, monday, tuesday, wednesday, thursday, friday, saturday, sunday, holidays_only, message: RestaurantOpeningSchedule(
         restaurant=name,
         start_date=start_date,
         end_date=end_date,
         monday=monday,
         tuesday=tuesday,
         wednesday=wednesday,
         thursday=thursday,
         friday=friday,
         saturday=saturday,
         sunday=sunday,
         holidays_only=holidays_only,
         message=message ),
      build_closure_override=lambda name, start_date, end_date, message: RestaurantScheduleOverride(
         restaurant=name,
         start_date=start_date,
         end_date=end_date,
         is_closed=True,
         message=message ),
      save_opening_schedule=lambda _conn, schedule: saved_schedules.append( schedule ) or True,
      save_schedule_override=lambda _conn, override: saved_overrides.append( override ) or True,
      save_replacing_overlaps=lambda _conn, schedule: replaced.append( schedule ) or True,
      save_trimming_overlaps=lambda _conn, schedule: trimmed.append( schedule ) or True )


@pytest.fixture
def stub_request_connection( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( RequestConnectionProvider, 'get', lambda: STUB_CONNECTION )


def Test_SetAsClosed_TestPayload_ExpectBuiltScheduleSaved(
      stub_request_connection: None,
) -> None:
   saved_schedules: list[ RestaurantOpeningSchedule ] = []

   mutations = _mutations(
      saved_schedules=saved_schedules,
      saved_overrides=[],
      replaced=[],
      trimmed=[] )

   assert mutations.set_as_closed( AMENITY_NAME, START_DATE, END_DATE, MESSAGE ) is True
   assert len( saved_schedules ) == 1
   assert saved_schedules[ 0 ].restaurant == AMENITY_NAME
   assert saved_schedules[ 0 ].message == MESSAGE


def Test_SetClosureOverride_TestPayload_ExpectOverrideSaved(
      stub_request_connection: None,
) -> None:
   saved_overrides: list[ RestaurantScheduleOverride ] = []

   mutations = _mutations(
      saved_schedules=[],
      saved_overrides=saved_overrides,
      replaced=[],
      trimmed=[] )

   assert mutations.set_closure_override( AMENITY_NAME, START_DATE, END_DATE, MESSAGE ) is True
   assert len( saved_overrides ) == 1
   assert saved_overrides[ 0 ].restaurant == AMENITY_NAME


def Test_ReplaceOpeningScheduleOverlaps_TestPayload_ExpectReplacePath(
      stub_request_connection: None,
) -> None:
   replaced: list[ RestaurantOpeningSchedule ] = []

   mutations = _mutations(
      saved_schedules=[],
      saved_overrides=[],
      replaced=replaced,
      trimmed=[] )

   assert mutations.replace_opening_schedule_overlaps(
      AMENITY_NAME,
      START_DATE,
      END_DATE,
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=MESSAGE ) is True

   assert len( replaced ) == 1
   assert replaced[ 0 ].monday is True


def Test_TrimOpeningScheduleOverlaps_TestPayload_ExpectTrimPath(
      stub_request_connection: None,
) -> None:
   trimmed: list[ RestaurantOpeningSchedule ] = []

   mutations = _mutations(
      saved_schedules=[],
      saved_overrides=[],
      replaced=[],
      trimmed=trimmed )

   assert mutations.trim_opening_schedule_overlaps(
      AMENITY_NAME,
      START_DATE,
      END_DATE,
      monday=False,
      tuesday=True,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      holidays_only=False,
      message=MESSAGE ) is True

   assert len( trimmed ) == 1
   assert trimmed[ 0 ].tuesday is True
