from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import LION_ITINERARY_ENTRY, wild_encounter_key
from itinerary.support import LION_KEY
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.itinerary_schedule_window_partitioner import ItineraryScheduleWindowPartitioner
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.itinerary_stop_resolver import ItineraryStopResolver
from api.itinerary.routing.itinerary_stop_resolver import ItineraryStopResolver
from api.shared.calendar_dates import DateValues
from api.shared.enums import ScheduleItemKind
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def _set_rhino_encounter_schedule() -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Guardians of White Rhinos',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=[
         wire_schedule_row( '11:00', monday=False, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=True, sunday=False ),
      ],
      message=None,
   )


def test_resolve_itinerary_stops_includes_entrance_and_animal_walk_nodes(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   stops = ItineraryStopResolver.resolve( itinerary )

   assert stops[ 0 ].schedule_item_kind == ScheduleItemKind.ENTRANCE
   assert stops[ 0 ].item_key == ENTRANCE_ITEM_KEY
   assert stops[ 0 ].walk_node_ids == [ 'v-0001' ]
   assert stops[ 0 ].x_coord == 61.414
   assert stops[ 0 ].y_coord == 91.366

   lion_stop = next(
      stop for stop in stops
      if stop.item_key == LION_KEY )
   assert lion_stop.schedule_item_kind == ScheduleItemKind.ANIMAL
   assert lion_stop.walk_node_ids
   assert all( walk_node_id.startswith( 'v-' ) for walk_node_id in lion_stop.walk_node_ids )


def test_resolve_itinerary_stops_maps_rhino_encounter_to_meeting_spot_walk_node(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_rhino_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( 'Guardians of White Rhinos', start_time='11:00' ) ],
      confirming_early_admission=True,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   encounter_stop = next(
      stop for stop in ItineraryStopResolver.resolve( itinerary )
      if stop.schedule_item_kind == ScheduleItemKind.WILD_ENCOUNTER )

   assert encounter_stop.item_key == 'Guardians of White Rhinos'
   assert encounter_stop.meeting_spot == 'Wild Encounter - Penguin Meeting Spot'
   assert len( encounter_stop.walk_node_ids ) == 1
   assert encounter_stop.walk_node_ids[ 0 ].startswith( 'v-' )
   assert encounter_stop.is_fixed_time
   assert encounter_stop.start_time == '11:00 AM'
   assert encounter_stop.end_time == '11:45 AM'


def test_partition_itinerary_schedule_windows_splits_around_fixed_encounter(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_rhino_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ wild_encounter_key( 'Guardians of White Rhinos', start_time='11:00' ) ],
      confirming_early_admission=True,
   ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   anchor_seconds = DateValues.time_value_in_seconds( itinerary.arrival_time )
   day_end_seconds = DateValues.time_value_in_seconds( itinerary.departure_time )

   assert anchor_seconds is not None
   assert day_end_seconds is not None

   windows = ItineraryScheduleWindowPartitioner.partition(
      anchor_seconds,
      day_end_seconds,
      ItineraryStopResolver.resolve_fixed_time( itinerary ) )

   assert len( windows ) == 2
   assert windows[ 0 ].start_seconds == anchor_seconds
   assert windows[ 0 ].end_seconds == DateValues.time_value_in_seconds( '11:00 AM' )
   assert windows[ 0 ].anchor_stop is not None
   assert windows[ 0 ].anchor_stop.item_key == 'Guardians of White Rhinos'
   assert windows[ 0 ].anchor_stop.walk_node_ids == [ 'v-0644' ]
   assert windows[ 1 ].start_seconds == DateValues.time_value_in_seconds( '11:45 AM' )
   assert windows[ 1 ].end_seconds == day_end_seconds
   assert windows[ 1 ].anchor_stop is None
