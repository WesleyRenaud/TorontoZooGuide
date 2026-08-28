from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry
from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import schedule_itinerary_item
from wild_encounter_schedule_support import wire_schedule_rows

from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.models import Itinerary
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers

OTTER_TALK = 'North American River Otter'
REGIONS = [
   'Africa',
   'Americas',
   'Australasia',
   'Canadian Domain',
   'Tundra Trek',
]


def _selected_exhibits_for_regions( region_names: list[ str ] ) -> list[ str ]:
   selected_exhibits: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name in region_names:
         selected_exhibits.extend( region.exhibits )

   assert selected_exhibits

   return selected_exhibits


def _set_saturday_otter_talk_schedule( *, talk_time: str = '14:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=OTTER_TALK,
      location='Americas Pavilion',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         talk_time,
         monday=False,
         tuesday=False,
         wednesday=False,
         thursday=False,
         friday=False,
         saturday=True,
         sunday=False ),
      message=None,
   )


def _unscheduled_americas_animals( itinerary: Itinerary ) -> list[ tuple[ str, str | None ] ]:
   return [
      ( animal.species, animal.enclosure_name )
      for animal in itinerary.animals
      if (
         animal.exhibit == 'Americas Pavilion'
         and not animal.covered_by_talk
         and (
            DateValues.normalize_schedule_time_key( animal.start_time ) is None
            or DateValues.normalize_schedule_time_key( animal.end_time ) is None
         )
      )
   ]


def test_bulk_schedule_reserves_before_otter_talk_for_americas_pavilion(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_otter_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         _selected_exhibits_for_regions( REGIONS ),
         visit_date='2026-06-20' ),
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( OTTER_TALK, start_time='14:00' ) ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_regions( REGIONS ),
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary(
      confirming_fixed_time_item_long_wait=True )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert _unscheduled_americas_animals( result.itinerary ) == []

   talk_start_seconds = DateValues.time_value_in_seconds( '2:00 PM' )
   talk_end_seconds = DateValues.time_value_in_seconds( '2:30 PM' )
   assert talk_start_seconds is not None
   assert talk_end_seconds is not None

   indoor_otter = next(
      animal
      for animal in result.itinerary.animals
      if (
         animal.species == OTTER_TALK
         and animal.enclosure_name == 'Indoor'
      )
   )
   assert indoor_otter.covered_by_talk

   before_talk_americas = [
      animal
      for animal in result.itinerary.animals
      if (
         animal.exhibit == 'Americas Pavilion'
         and not animal.covered_by_talk
         and DateValues.time_value_in_seconds( animal.end_time ) is not None
         and DateValues.time_value_in_seconds( animal.end_time ) <= talk_start_seconds
      )
   ]
   after_talk_americas = [
      animal
      for animal in result.itinerary.animals
      if (
         animal.exhibit == 'Americas Pavilion'
         and not animal.covered_by_talk
         and DateValues.time_value_in_seconds( animal.start_time ) is not None
         and DateValues.time_value_in_seconds( animal.start_time ) >= talk_end_seconds
      )
   ]

   assert before_talk_americas
   assert after_talk_americas


def test_adding_otter_talk_after_bulk_keeps_americas_pavilion_scheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_otter_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         _selected_exhibits_for_regions( REGIONS ),
         visit_date='2026-06-20' ),
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_regions( REGIONS ),
      confirming_early_admission=True,
   ).success

   bulk = ItineraryCoordinator.bulk_schedule_itinerary()
   assert bulk.success
   assert bulk.status == ItineraryErrorType.SUCCESS

   result = schedule_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK,
      GuardiansTalkScheduleItemKey(
         name=OTTER_TALK,
         start_time='14:00',
         end_time=None ).to_wire(),
      confirming_guardians_talk_unschedule=True,
      confirming_guardians_talk_without_animal=True,
      confirming_fixed_time_item_long_wait=True,
   )

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert _unscheduled_americas_animals( result.itinerary ) == []
