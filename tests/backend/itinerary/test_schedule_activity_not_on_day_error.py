from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import LION_ITINERARY_ENTRY, schedule_itinerary_item, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_wire

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers


def test_schedule_wild_encounter_not_on_day_returns_typed_error(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   set_wild_encounter_schedule( encounter_time='15:30' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      wild_encounter_wire( WILD_ENCOUNTER, start_time='15:30' ),
   )

   assert not result.success
   assert result.status == ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE
