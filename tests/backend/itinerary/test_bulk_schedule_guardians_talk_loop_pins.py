from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import guardians_talk_save_entry
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.guardians.scheduling.guardians_talk_loop_schedule_pin import viewing_spot_index_for_talk_in_loop
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.guardians_talk_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.routing.partition_itinerary_schedule_windows import partition_itinerary_schedule_windows
from api.itinerary.routing.resolve_itinerary_stops import resolve_fixed_time_itinerary_stops
from api.itinerary.routing.resolve_itinerary_stops import resolve_itinerary_stops
from api.itinerary.scheduling.bulk.bulk_schedule_loop_pins import attach_loop_pins_to_schedule_windows
from api.itinerary.scheduling.bulk.bulk_schedule_loop_pins import separate_schedule_boundaries_and_loop_pins
from api.itinerary.scheduling.bulk.schedule_loop_unit_with_pins import viewing_spot_index_for_animal_in_loop
from api.models import Animal
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from api.walk_graph.master_route import default_master_route_loop_by_id
from conftest import DbControllers

AFRICAN_LION_TALK = 'African Lion'
AFRICA_SAVANNA = 'Africa Savanna'


def _animal_viewing_spot_index(
      loop_id: str,
      animal: Animal ) -> int | None:
   return viewing_spot_index_for_animal_in_loop(
      loop_id,
      ItineraryAnimalRecord(
         species=animal.species,
         exhibit=animal.exhibit,
         enclosure_name=animal.enclosure_name,
         old_likelihood=None,
         new_likelihood=100,
      ) )


def _set_saturday_african_lion_talk_schedule(
      *,
      talk_time: str = '11:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=AFRICAN_LION_TALK,
      location=AFRICA_SAVANNA,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( talk_time, monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=True, sunday=False ),
      message=None,
   )


def test_resolve_guardians_talk_loop_pin_maps_african_lion_to_savanna_loop() -> None:
   master_route_loop = default_master_route_loop_by_id()[ 'africa_savanna_canadian_domain' ]
   viewing_spot_index = viewing_spot_index_for_talk_in_loop(
      master_route_loop,
      talk_name=AFRICAN_LION_TALK,
      talk_location=AFRICA_SAVANNA )

   assert viewing_spot_index is not None
   assert master_route_loop.viewing_spots[ viewing_spot_index ].species == AFRICAN_LION_TALK


def test_partition_keeps_loop_pin_talk_inside_single_schedule_window(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_african_lion_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( AFRICAN_LION_TALK, start_time='11:00' ) ],
      wild_encounters=[],
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   anchor_seconds = DateValues.time_value_in_seconds( itinerary.arrival_time )
   day_end_seconds = DateValues.time_value_in_seconds( itinerary.departure_time )

   assert anchor_seconds is not None
   assert day_end_seconds is not None

   fixed_time_stops = resolve_fixed_time_itinerary_stops( itinerary )
   boundary_stops, loop_pins = separate_schedule_boundaries_and_loop_pins(
      db.conn,
      itinerary,
      fixed_time_stops )
   windows = attach_loop_pins_to_schedule_windows(
      partition_itinerary_schedule_windows(
         anchor_seconds,
         day_end_seconds,
         boundary_stops ),
      loop_pins )

   talk_start_seconds = DateValues.time_value_in_seconds( '11:00 AM' )
   talk_end_seconds = DateValues.time_value_in_seconds( '11:30 AM' )

   assert talk_start_seconds is not None
   assert talk_end_seconds is not None
   assert len( loop_pins ) == 1
   assert loop_pins[ 0 ].loop_id == 'africa_savanna_canadian_domain'
   assert len( boundary_stops ) == 1
   assert boundary_stops[ 0 ].item_key == AFRICAN_LION_TALK
   assert len( windows ) == 2
   assert windows[ 0 ].start_seconds == anchor_seconds
   assert windows[ 0 ].end_seconds == talk_start_seconds
   assert windows[ 1 ].start_seconds == talk_end_seconds
   assert windows[ 1 ].end_seconds == day_end_seconds
   assert len( windows[ 0 ].loop_pins ) == 1
   assert len( windows[ 1 ].loop_pins ) == 1
   assert windows[ 0 ].loop_pins[ 0 ].stop.item_key == AFRICAN_LION_TALK


def test_bulk_schedule_weaves_african_lion_talk_into_africa_savanna_loop(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_african_lion_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( AFRICAN_LION_TALK, start_time='11:00' ) ],
      wild_encounters=[],
      selected_exhibits=[ AFRICA_SAVANNA ],
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   talk_start_seconds = DateValues.time_value_in_seconds( '11:00 AM' )
   talk_end_seconds = DateValues.time_value_in_seconds( '11:30 AM' )
   loop_id = 'africa_savanna_canadian_domain'
   lion_pin_index = viewing_spot_index_for_talk_in_loop(
      default_master_route_loop_by_id()[ loop_id ],
      talk_name=AFRICAN_LION_TALK,
      talk_location=AFRICA_SAVANNA )

   assert talk_start_seconds is not None
   assert talk_end_seconds is not None
   assert lion_pin_index is not None

   scheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if (
         animal.start_time is not None
         and animal.end_time is not None
         and not animal.covered_by_talk )
   ]

   assert scheduled_animals

   before_talk = [
      animal
      for animal in scheduled_animals
      if (
         ( animal_index := _animal_viewing_spot_index( loop_id, animal ) ) is not None
         and animal_index <= lion_pin_index
      )
   ]
   after_talk = [
      animal
      for animal in scheduled_animals
      if (
         ( animal_index := _animal_viewing_spot_index( loop_id, animal ) ) is not None
         and animal_index > lion_pin_index
      )
   ]

   assert before_talk
   assert after_talk

   assert all(
      DateValues.time_value_in_seconds( animal.end_time ) <= talk_start_seconds
      for animal in before_talk
      if DateValues.time_value_in_seconds( animal.end_time ) is not None )

   penguin = next(
      animal for animal in scheduled_animals
      if animal.species == 'African Penguin' )
   cheetah = next(
      animal for animal in scheduled_animals
      if animal.species == 'Cheetah' and animal.exhibit == AFRICA_SAVANNA )

   penguin_index = _animal_viewing_spot_index( loop_id, penguin )
   cheetah_index = _animal_viewing_spot_index( loop_id, cheetah )

   assert penguin_index is not None
   assert cheetah_index is not None
   assert penguin_index <= lion_pin_index
   assert cheetah_index > lion_pin_index

   penguin_end_seconds = DateValues.time_value_in_seconds( penguin.end_time )
   cheetah_start_seconds = DateValues.time_value_in_seconds( cheetah.start_time )

   assert penguin_end_seconds is not None
   assert cheetah_start_seconds is not None
   assert penguin_end_seconds <= talk_start_seconds
   assert cheetah_start_seconds >= talk_end_seconds


HYENA_TALK = 'Spotted Hyena'
MULTI_REGION_NAMES = [
   'Africa',
   'Indo-Malaya',
   'Tundra Trek',
]


def _selected_exhibits_for_regions(
      region_names: list[ str ] ) -> list[ str ]:
   from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator

   selected_exhibits: list[ str ] = []

   for region in ExhibitCoordinator.get_regions_with_exhibits():
      if region.name in region_names:
         selected_exhibits.extend( region.exhibits )

   assert selected_exhibits

   return selected_exhibits


def _set_saturday_hyena_talk_schedule(
      *,
      talk_time: str = '13:00' ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=HYENA_TALK,
      location=AFRICA_SAVANNA,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( talk_time, monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=True, sunday=False ),
      message=None,
   )


def test_bulk_schedule_does_not_overlap_loop_pin_guardians_talk(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_hyena_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( HYENA_TALK, start_time='13:00' ) ],
      wild_encounters=[],
      selected_exhibits=_selected_exhibits_for_regions( MULTI_REGION_NAMES ),
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []

   talk = next(
      guardians_talk
      for guardians_talk in result.itinerary.guardians_talks
      if guardians_talk.name == HYENA_TALK )
   talk_start_seconds = DateValues.time_value_in_seconds( talk.start_time )
   talk_end_seconds = DateValues.time_value_in_seconds( talk.end_time )

   assert talk_start_seconds is not None
   assert talk_end_seconds is not None

   for animal in result.itinerary.animals:
      if animal.covered_by_talk:
         continue

      animal_start_seconds = DateValues.time_value_in_seconds( animal.start_time )
      animal_end_seconds = DateValues.time_value_in_seconds( animal.end_time )

      if animal_start_seconds is None or animal_end_seconds is None:
         continue

      assert not (
         animal_start_seconds < talk_end_seconds
         and talk_start_seconds < animal_end_seconds )

   unscheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.start_time is None or animal.end_time is None
   ]

   assert unscheduled_animals == []


def test_bulk_schedule_covers_african_lion_animal_when_talk_is_woven(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_african_lion_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( AFRICAN_LION_TALK, start_time='11:00' ) ],
      wild_encounters=[],
      selected_exhibits=[ AFRICA_SAVANNA ],
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   lion = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == AFRICAN_LION_TALK and animal.exhibit == AFRICA_SAVANNA )

   assert lion.covered_by_talk is True
   assert lion.start_time == '11:00 AM'
   assert lion.end_time == '11:30 AM'

   animal_stops = [
      stop
      for stop in resolve_itinerary_stops( result.itinerary )
      if (
         stop.schedule_item_kind == ScheduleItemKind.ANIMAL
         and AFRICAN_LION_TALK in stop.item_key )
   ]

   assert animal_stops == []


def test_unschedule_woven_talk_restores_enclosure_at_default_duration_and_shifts_later_items(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_african_lion_talk_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( AFRICAN_LION_TALK, start_time='11:00' ) ],
      wild_encounters=[],
      selected_exhibits=[ AFRICA_SAVANNA ],
      confirming_early_admission=True,
      confirming_guardians_talk_without_animal=True,
   ).success

   scheduled = ItineraryCoordinator.bulk_schedule_animals()

   assert scheduled.success

   cheetah_before = next(
      animal
      for animal in scheduled.itinerary.animals
      if animal.species == 'Cheetah' and animal.exhibit == AFRICA_SAVANNA )
   cheetah_start_before = DateValues.time_value_in_seconds( cheetah_before.start_time )

   assert cheetah_start_before is not None
   assert cheetah_start_before >= DateValues.time_value_in_seconds( '11:30 AM' )

   result = ItineraryCoordinator.unschedule_itinerary_item(
      GuardiansTalkScheduleItemKey(
         name=AFRICAN_LION_TALK,
         start_time='11:00' ) )

   assert result.success

   lion = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == AFRICAN_LION_TALK and animal.exhibit == AFRICA_SAVANNA )
   cheetah_after = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Cheetah' and animal.exhibit == AFRICA_SAVANNA )

   assert lion.covered_by_talk is False
   assert lion.start_time == '11:00 AM'
   assert lion.end_time == '11:08 AM'

   cheetah_start_after = DateValues.time_value_in_seconds( cheetah_after.start_time )

   assert cheetah_start_after is not None
   assert cheetah_start_after == cheetah_start_before - 22 * 60
