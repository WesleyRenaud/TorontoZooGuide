from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits
from itinerary.support import wild_encounter_key
from wild_encounter_schedule_support import wire_schedule_rows

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.scheduling.bulk.loop_pin_segments import viewing_spot_index_for_stop_in_loop
from api.models import Animal
from api.models import WildEncounter
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ScheduleItemKind
from api.walk_graph.master_route import default_master_route_loop_by_id
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from api.wild_encounters.data_access.wild_encounter_meeting_spot_loop_pin import fetch_wild_encounter_meeting_spot_loop_pins_by_name
from api.wild_encounters.scheduling.wild_encounter_loop_schedule_pin import resolve_wild_encounter_loop_pin
from conftest import DbControllers

AFRICA_SAVANNA = 'Africa Savanna'
CANADIAN_DOMAIN_MEETING_SPOT = 'Wild Encounter - Canadian Domain Meeting Spot'
CANADIAN_DOMAIN_SAVANNA_LOOP = 'africa_savanna_canadian_domain'
GRIZZLY_BEAR_ENCOUNTER = 'Grizzly Bear'
MAYAN_TEMPLE_MEETING_SPOT = 'Wild Encounter - Mayan Temple Meeting Spot'
TUNDRA_TREK_MAYAN_TEMPLE_LOOP = 'tundra_trek_mayan_temple'


def _animal_viewing_spot_index(
      loop_id: str,
      animal: Animal ) -> int | None:
   return viewing_spot_index_for_stop_in_loop(
      loop_id,
      ItineraryAnimalRecord(
         species=animal.species,
         exhibit=animal.exhibit,
         enclosure_name=animal.enclosure_name,
         old_likelihood=None,
         new_likelihood=100,
      ) )


def _set_saturday_grizzly_encounter_schedule(
      *,
      encounter_time: str = '13:00' ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=GRIZZLY_BEAR_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         encounter_time,
         monday=False,
         saturday=True ),
      message=None,
   )


def test_resolve_wild_encounter_loop_pin_returns_none_for_unpinned_meeting_spot(
      db: DbControllers ) -> None:
   meeting_spot_loop_pins_by_name = fetch_wild_encounter_meeting_spot_loop_pins_by_name(
      db.conn )
   wild_encounter = WildEncounter(
      name='Guardians of White Rhinos',
      meeting_spot='Wild Encounter - Penguin Meeting Spot',
      link='https://example.com',
      start_time='10:00 AM',
      end_time='10:45 AM' )
   itinerary_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key='Guardians of White Rhinos',
      meeting_spot='Wild Encounter - Penguin Meeting Spot',
      walk_node_ids=( 'v-0001', ),
      is_fixed_time=True,
      start_time='10:00 AM',
      end_time='10:45 AM' )

   assert resolve_wild_encounter_loop_pin(
      wild_encounter,
      itinerary_stop,
      meeting_spot_loop_pins_by_name=meeting_spot_loop_pins_by_name ) is None


def test_resolve_wild_encounter_loop_pin_maps_canadian_domain_between_zebra_and_raccoon(
      db: DbControllers ) -> None:
   meeting_spot_loop_pins_by_name = fetch_wild_encounter_meeting_spot_loop_pins_by_name(
      db.conn )
   meeting_spot_loop_pin = meeting_spot_loop_pins_by_name[
      CANADIAN_DOMAIN_MEETING_SPOT ]
   master_route_loop = default_master_route_loop_by_id()[
      meeting_spot_loop_pin.loop_id ]

   assert meeting_spot_loop_pin.loop_viewing_spot_index == 6
   assert (
         master_route_loop.viewing_spots[ 6 ].species == "Grevy's Zebra"
         and master_route_loop.viewing_spots[ 6 ].exhibit == 'Canadian Domain' )
   assert master_route_loop.viewing_spots[ 7 ].species == 'Raccoon'

   wild_encounter = WildEncounter(
      name=GRIZZLY_BEAR_ENCOUNTER,
      meeting_spot=CANADIAN_DOMAIN_MEETING_SPOT,
      link='https://example.com',
      start_time='1:00 PM',
      end_time='1:45 PM' )
   itinerary_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
      item_key=GRIZZLY_BEAR_ENCOUNTER,
      meeting_spot=CANADIAN_DOMAIN_MEETING_SPOT,
      walk_node_ids=( 'v-0611', ),
      is_fixed_time=True,
      start_time='1:00 PM',
      end_time='1:45 PM' )

   loop_pin = resolve_wild_encounter_loop_pin(
      wild_encounter,
      itinerary_stop,
      meeting_spot_loop_pins_by_name=meeting_spot_loop_pins_by_name )

   assert loop_pin is not None
   assert loop_pin.loop_id == CANADIAN_DOMAIN_SAVANNA_LOOP
   assert loop_pin.viewing_spot_index == 6


def test_resolve_wild_encounter_loop_pin_maps_mayan_temple_encounters_to_tundra_loop(
      db: DbControllers ) -> None:
   meeting_spot_loop_pins_by_name = fetch_wild_encounter_meeting_spot_loop_pins_by_name(
      db.conn )
   meeting_spot_loop_pin = meeting_spot_loop_pins_by_name[
      MAYAN_TEMPLE_MEETING_SPOT ]

   assert meeting_spot_loop_pin.loop_id == TUNDRA_TREK_MAYAN_TEMPLE_LOOP
   assert meeting_spot_loop_pin.loop_viewing_spot_index == 3

   for encounter_name in ( 'Capybara', 'From Howls to Honks' ):
      wild_encounter = WildEncounter(
         name=encounter_name,
         meeting_spot=MAYAN_TEMPLE_MEETING_SPOT,
         link='https://example.com',
         start_time='11:00 AM',
         end_time='11:30 AM' )
      itinerary_stop = ItineraryStop(
         schedule_item_kind=ScheduleItemKind.WILD_ENCOUNTER,
         item_key=encounter_name,
         meeting_spot=MAYAN_TEMPLE_MEETING_SPOT,
         walk_node_ids=( 'v-0825', ),
         is_fixed_time=True,
         start_time='11:00 AM',
         end_time='11:30 AM' )

      loop_pin = resolve_wild_encounter_loop_pin(
         wild_encounter,
         itinerary_stop,
         meeting_spot_loop_pins_by_name=meeting_spot_loop_pins_by_name )

      assert loop_pin is not None
      assert loop_pin.loop_id == TUNDRA_TREK_MAYAN_TEMPLE_LOOP
      assert loop_pin.viewing_spot_index == 3


def test_bulk_schedule_weaves_grizzly_encounter_into_africa_savanna_loop(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_grizzly_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         [ AFRICA_SAVANNA ],
         visit_date='2026-06-20' ),
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( GRIZZLY_BEAR_ENCOUNTER, start_time='13:00' ) ],
      selected_exhibits=[ AFRICA_SAVANNA ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS

   encounter_start_seconds = DateValues.time_value_in_seconds( '1:00 PM' )
   encounter_end_seconds = DateValues.time_value_in_seconds( '1:45 PM' )
   loop_id = CANADIAN_DOMAIN_SAVANNA_LOOP
   encounter_pin_index = fetch_wild_encounter_meeting_spot_loop_pins_by_name(
      db.conn )[ CANADIAN_DOMAIN_MEETING_SPOT ].loop_viewing_spot_index

   assert encounter_start_seconds is not None
   assert encounter_end_seconds is not None

   scheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.start_time is not None and animal.end_time is not None
   ]

   assert scheduled_animals

   before_encounter = [
      animal
      for animal in scheduled_animals
      if (
         ( animal_index := _animal_viewing_spot_index( loop_id, animal ) ) is not None
         and animal_index <= encounter_pin_index
      )
   ]
   after_encounter = [
      animal
      for animal in scheduled_animals
      if (
         ( animal_index := _animal_viewing_spot_index( loop_id, animal ) ) is not None
         and animal_index > encounter_pin_index
      )
   ]

   assert before_encounter
   assert after_encounter

   assert encounter_pin_index == 6

   zebra_viewing_spot = default_master_route_loop_by_id()[ loop_id ].viewing_spots[ 6 ]
   raccoon_viewing_spot = default_master_route_loop_by_id()[ loop_id ].viewing_spots[ 7 ]

   assert zebra_viewing_spot.species == "Grevy's Zebra"
   assert raccoon_viewing_spot.species == 'Raccoon'

   hyena = next(
      animal for animal in scheduled_animals
      if animal.species == 'Spotted Hyena' )
   cheetah = next(
      animal for animal in scheduled_animals
      if animal.species == 'Cheetah' and animal.exhibit == AFRICA_SAVANNA )

   hyena_index = _animal_viewing_spot_index( loop_id, hyena )
   cheetah_index = _animal_viewing_spot_index( loop_id, cheetah )

   assert hyena_index is not None
   assert cheetah_index is not None
   assert hyena_index <= encounter_pin_index
   assert cheetah_index > encounter_pin_index

   hyena_end_seconds = DateValues.time_value_in_seconds( hyena.end_time )
   cheetah_start_seconds = DateValues.time_value_in_seconds( cheetah.start_time )

   assert hyena_end_seconds is not None
   assert cheetah_start_seconds is not None
   assert hyena_end_seconds >= encounter_end_seconds
   assert cheetah_start_seconds >= encounter_end_seconds


def test_bulk_schedule_does_not_overlap_loop_pin_wild_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_saturday_grizzly_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=itinerary_animals_for_exhibits(
         [ AFRICA_SAVANNA ],
         visit_date='2026-06-20' ),
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( GRIZZLY_BEAR_ENCOUNTER, start_time='13:00' ) ],
      selected_exhibits=[ AFRICA_SAVANNA ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []

   encounter = next(
      wild_encounter
      for wild_encounter in result.itinerary.wild_encounters
      if wild_encounter.name == GRIZZLY_BEAR_ENCOUNTER )
   encounter_start_seconds = DateValues.time_value_in_seconds( encounter.start_time )
   encounter_end_seconds = DateValues.time_value_in_seconds( encounter.end_time )

   assert encounter_start_seconds is not None
   assert encounter_end_seconds is not None

   for animal in result.itinerary.animals:
      animal_start_seconds = DateValues.time_value_in_seconds( animal.start_time )
      animal_end_seconds = DateValues.time_value_in_seconds( animal.end_time )

      if animal_start_seconds is None or animal_end_seconds is None:
         continue

      assert not (
         animal_start_seconds < encounter_end_seconds
         and encounter_start_seconds < animal_end_seconds )

   unscheduled_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.start_time is None or animal.end_time is None
   ]

   assert unscheduled_animals == []
