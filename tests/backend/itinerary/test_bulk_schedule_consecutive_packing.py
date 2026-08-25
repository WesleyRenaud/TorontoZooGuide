from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import entrance_travel_seconds_to_animal
from itinerary.support import expected_departure_time_for_itinerary
from itinerary.support import guardians_talk_save_entry
from itinerary.support import guardians_talk_wire
from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import schedule_time_before_seconds
from itinerary.support import unschedule_itinerary_item
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.models import Itinerary
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers

ZEBRA_TALK = "Grevy's Zebra"
AFRICA_SAVANNA = 'Africa Savanna'


def _expected_arrival_from_earliest_animal( itinerary: Itinerary ) -> str:
   scheduled_animals = [
      animal
      for animal in itinerary.animals
      if animal.start_time is not None
      and animal.end_time is not None
      and not animal.covered_by_talk
   ]
   earliest = min(
      scheduled_animals,
      key=lambda animal: DateValues.time_value_in_seconds( animal.start_time ) or 0 )
   travel_seconds = entrance_travel_seconds_to_animal(
      species=earliest.species,
      exhibit=earliest.exhibit,
      enclosure_name=earliest.enclosure_name )

   return schedule_time_before_seconds( earliest.start_time, travel_seconds )


def _selected_exhibits_for_africa_savanna() -> list[ str ]:
   from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if AFRICA_SAVANNA in region.exhibits:
         return [ AFRICA_SAVANNA ]

   raise AssertionError( f'{ AFRICA_SAVANNA } exhibit not found in seed data' )


def _set_saturday_zebra_talk_schedule(
      *,
      talk_time: str = '11:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=ZEBRA_TALK,
      location=AFRICA_SAVANNA,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( talk_time, monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=True, sunday=False ),
      message=None,
   )


def test_bulk_schedule_packs_non_pinned_loops_before_guardians_talk_and_shifts_arrival(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_zebra_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         _selected_exhibits_for_africa_savanna(),
         visit_date='2026-06-20' ),
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time='11:00' ) ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_africa_savanna(),
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []
   assert result.adjustments == []
   assert result.itinerary.arrival_time == _expected_arrival_from_earliest_animal(
      result.itinerary )

   giraffe = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Masai Giraffe'
      and animal.enclosure_name == 'Outdoor' )
   talk = next(
      talk for talk in result.itinerary.guardians_talks
      if talk.name == ZEBRA_TALK )

   arrival_seconds = DateValues.time_value_in_seconds(
      result.itinerary.arrival_time )
   giraffe_start_seconds = DateValues.time_value_in_seconds( giraffe.start_time )
   talk_start_seconds = DateValues.time_value_in_seconds( talk.start_time )

   assert arrival_seconds is not None
   assert giraffe_start_seconds is not None
   assert talk_start_seconds is not None

   assert giraffe_start_seconds >= arrival_seconds
   assert giraffe_start_seconds < talk_start_seconds

   scheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   ]

   assert scheduled_animals

   earliest_start_seconds = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in scheduled_animals )

   assert earliest_start_seconds >= arrival_seconds

   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def _schedule_africa_savanna_with_zebra_talk(
      *,
      talk_time: str = '11:00' ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         _selected_exhibits_for_africa_savanna(),
         visit_date='2026-06-20' ),
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( ZEBRA_TALK, start_time=talk_time ) ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_africa_savanna(),
      confirming_early_admission=True,
   ).success


def test_bulk_schedule_keeps_arrival_after_pinned_talk_removed_and_rescheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_zebra_talk_schedule()
   _schedule_africa_savanna_with_zebra_talk()

   with_talk = ItineraryCoordinator.bulk_schedule_itinerary()

   assert with_talk.success
   assert with_talk.adjustments == []
   assert with_talk.itinerary.arrival_time == _expected_arrival_from_earliest_animal(
      with_talk.itinerary )

   assert unschedule_itinerary_item(
      item_type='guardians_talks',
      key=guardians_talk_wire( ZEBRA_TALK, start_time='11:00' ),
   ).success

   without_talk = ItineraryCoordinator.bulk_schedule_itinerary()

   assert without_talk.success
   assert without_talk.itinerary.arrival_time == (
      _expected_arrival_from_earliest_animal( without_talk.itinerary ) )

   scheduled_animals = [
      animal
      for animal in without_talk.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   ]

   earliest_start_seconds = min(
      DateValues.time_value_in_seconds( animal.start_time )
      for animal in scheduled_animals )
   arrival_seconds = DateValues.time_value_in_seconds(
      without_talk.itinerary.arrival_time )

   assert earliest_start_seconds is not None
   assert arrival_seconds is not None
   assert earliest_start_seconds >= arrival_seconds
