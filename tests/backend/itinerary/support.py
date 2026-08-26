from __future__ import annotations

from collections.abc import Callable
from datetime import date

from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.guardians_talk_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.routing.walk_travel_time import travel_time_seconds_between_nodes
from api.itinerary.scheduling.core.time_block import latest_scheduled_end_seconds
from api.itinerary.scheduling.items.map_schedule_item_key_from_wire import map_schedule_item_key_from_wire
from api.itinerary.scheduling.items.schedule_item_key import ScheduleItemKey
from api.itinerary.scheduling.items.schedule_item_travel_time import entrance_travel_seconds_from_latest_item
from api.itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
from api.models import Itinerary
from api.shared.calendar_dates import DateValues
from api.shared.constants import ITINERARY_ANIMAL_MIN_LIKELIHOOD
from api.types import DateInput
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.domain.map_location_kind import MapLocationKind
from api.walk_graph.map_location_walk_node_lookup import walk_node_for_map_location
from api.walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers

GUARDIANS_TALK = 'African Lion'
WILD_ENCOUNTER = 'African Rainforest'
WILD_ENCOUNTER_TIME = '14:00'
TURTLE_TALK = 'Nile Soft-Shelled Turtle'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'
RHINO_ENCOUNTER_TIME = '14:00'
CAROUSEL = 'Conservation Carousel'
LION_KEY = 'African Lion||Africa Savanna'
ANIMAL_KEY = LION_KEY
PENGUIN_KEY = 'African Penguin||Africa Savanna||Outdoor'
CHEETAH_KEY = 'Cheetah||Africa Savanna'
LION_ITINERARY_ENTRY = {
   'species': 'African Lion',
   'exhibit': 'Africa Savanna',
}
PENGUIN_ITINERARY_ENTRY = {
   'species': 'African Penguin',
   'exhibit': 'Africa Savanna',
   'enclosure_name': 'Outdoor',
}
CHEETAH_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Africa Savanna',
}
CHEETAH_INDO_MALAYA_ITINERARY_ENTRY = {
   'species': 'Cheetah',
   'exhibit': 'Indo-Malaya Outdoor',
}


def itinerary_animals_for_exhibits(
      exhibits: list[ str ],
      *,
      visit_date: DateInput,
      visit_date_temp: float | None = None ) -> list[ dict[ str, str | None ] ]:
   parsed_date = DateValues.parse_date_value( visit_date )
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=parsed_date.day,
      month=parsed_date.month,
      year=parsed_date.year,
      temp=visit_date_temp,
      include_off_display_animals=False,
      for_itinerary=True,
      threshold=ITINERARY_ANIMAL_MIN_LIKELIHOOD,
      exhibits_to_include=exhibits )

   animal_inputs: list[ dict[ str, str | None ] ] = []

   for animal in animals:
      if animal.exhibit == None:
         continue

      entry: dict[ str, str | None ] = {
         'species': animal.species,
         'exhibit': animal.exhibit,
      }

      if animal.enclosure_name:
         entry[ 'enclosure_name' ] = animal.enclosure_name

      animal_inputs.append( entry )

   return animal_inputs


def guardians_talk_save_entry(
      name: str,
      *,
      start_time: str | None = None,
      end_time: str | None = None ) -> dict[ str, str | None ]:
   return {
      'name': name,
      'start_time': start_time,
      'end_time': end_time,
   }


def wild_encounter_save_entry(
      name: str,
      *,
      start_time: str,
      end_time: str | None = None ) -> str:
   return WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time=end_time ).to_wire()


def guardians_talk_save_entries(
      *names: str,
      start_time: str,
      end_time: str | None = None ) -> list[ dict[ str, str | None ] ]:
   return [
      guardians_talk_save_entry(
         name,
         start_time=start_time,
         end_time=end_time )
      for name in names
   ]


def wild_encounter_save_entries(
      name: str,
      *,
      start_time: str,
      end_time: str | None = None ) -> list[ str ]:
   return [
      wild_encounter_save_entry( name, start_time=start_time, end_time=end_time )
   ]


def wild_encounter_keys(
      *names: str,
      start_time: str = WILD_ENCOUNTER_TIME,
      end_time: str | None = None ) -> list[ WildEncounterScheduleItemKey ]:
   return [
      wild_encounter_key( name, start_time=start_time, end_time=end_time )
      for name in names
   ]


def wild_encounter_key(
      name: str,
      *,
      start_time: str = WILD_ENCOUNTER_TIME,
      end_time: str | None = None ) -> WildEncounterScheduleItemKey:
   return WildEncounterScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time=end_time )


def wild_encounter_wire(
      name: str,
      *,
      start_time: str = WILD_ENCOUNTER_TIME,
      end_time: str | None = None ) -> str:
   return wild_encounter_key(
      name,
      start_time=start_time,
      end_time=end_time ).to_wire()


def guardians_talk_wire(
      name: str,
      *,
      start_time: str,
      end_time: str | None = None ) -> str:
   return GuardiansTalkScheduleItemKey(
      name=name,
      start_time=start_time,
      end_time=end_time ).to_wire()


def parsed_schedule_item(
      item_type: str,
      wire_key: str ) -> ScheduleItemKey | None:
   return map_schedule_item_key_from_wire( item_type, wire_key )


def schedule_itinerary_item(
      item_type: str,
      wire_key: str | None = None,
      *,
      key: str | None = None,
      **kwargs: object ) -> ItinerarySaveResult:
   return ItineraryCoordinator.schedule_itinerary_item(
      parsed_schedule_item(
         item_type,
         _resolved_wire_key( wire_key, key ) ),
      **kwargs )


def entrance_travel_seconds_to_animal(
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None = None ) -> int:
   walk_graph = load_walk_graph()
   walk_node_id = walk_node_id_for_viewing_spot(
      species,
      exhibit,
      enclosure_name )

   if walk_node_id is None:
      return 0

   return travel_time_seconds_between_nodes(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      walk_node_id )


def entrance_travel_seconds_to_map_location(
      kind: MapLocationKind,
      name: str ) -> int:
   walk_graph = load_walk_graph()
   walk_node = walk_node_for_map_location( kind, name )

   if walk_node is None:
      return 0

   return travel_time_seconds_between_nodes(
      walk_graph,
      walk_graph[ 'entrance_node_id' ],
      walk_node.walk_node_id )


def expected_departure_time_for_itinerary( itinerary: Itinerary ) -> str:
   latest_end_seconds = latest_scheduled_end_seconds( itinerary )
   assert latest_end_seconds is not None
   departure_time = DateValues.schedule_time_key_from_seconds(
      latest_end_seconds
      + entrance_travel_seconds_from_latest_item( itinerary ) )
   assert departure_time is not None
   return departure_time


def schedule_time_after_seconds(
      start_time: str,
      offset_seconds: int ) -> str:
   start_seconds = DateValues.time_value_in_seconds( start_time )
   assert start_seconds is not None
   result = DateValues.schedule_time_key_from_seconds(
      start_seconds + offset_seconds )
   assert result is not None
   return result


def schedule_time_before_seconds(
      start_time: str,
      offset_seconds: int ) -> str:
   return schedule_time_after_seconds( start_time, -offset_seconds )


def _resolved_wire_key(
      wire_key: str | None,
      key: str | None ) -> str:
   resolved_key = wire_key if wire_key is not None else key

   if resolved_key is None:
      raise TypeError( 'wire_key or key is required' )

   return resolved_key


def unschedule_itinerary_item(
      item_type: str,
      wire_key: str | None = None,
      *,
      key: str | None = None ) -> ItinerarySaveResult:
   return ItineraryCoordinator.unschedule_itinerary_item(
      parsed_schedule_item(
         item_type,
         _resolved_wire_key( wire_key, key ) ) )


def remove_itinerary_item(
      item_type: str,
      wire_key: str | None = None,
      *,
      key: str | None = None ) -> ItinerarySaveResult:
   return ItineraryCoordinator.remove_itinerary_item(
      parsed_schedule_item(
         item_type,
         _resolved_wire_key( wire_key, key ) ) )


def set_wild_encounter_schedule( *, encounter_time: str ) -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( encounter_time ),
      message=None,
   )


def set_guardians_talk_schedule( *, talk_time: str ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows(
         talk_time,
         monday=True,
         tuesday=True,
         wednesday=True,
         thursday=True,
         friday=True,
         saturday=True,
         sunday=True ),
      message=None,
   )


def set_guardians_talk_and_wild_encounter_schedules_at_1400() -> None:
   set_guardians_talk_schedule( talk_time='14:00' )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=WILD_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None,
   )


def set_itinerary_with_lion_scheduled_at_1400(
      *,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='14:00',
   ).success


def set_turtle_talk_and_rhino_encounter_schedules_at_1400() -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=TURTLE_TALK,
      location='African Rainforest Pavilion',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None,
   )
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name=RHINO_ENCOUNTER,
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '14:00' ),
      message=None,
   )


def set_itinerary_with_turtle_talk_and_lion_at_1430(
      *,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='guardians_talks',
      key=guardians_talk_wire( TURTLE_TALK, start_time='14:00' ),
      confirming_guardians_talk_without_animal=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='14:30',
      duration_minutes=15,
   ).success


def saved_animal_row(
      db: DbControllers,
      *,
      species: str,
      exhibit: str ) -> ItineraryAnimalRecord:
   saved_itinerary = ItineraryProvider.fetch_saved_itinerary( db.conn )

   for row in saved_itinerary.animal_rows:
      if row.species == species and row.exhibit == exhibit:
         return row

   raise AssertionError(
      f'Expected saved animal row for { species } / { exhibit }' )
