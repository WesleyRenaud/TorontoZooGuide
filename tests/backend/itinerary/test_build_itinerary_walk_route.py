from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import ANIMAL_KEY
from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY
from itinerary.support import LION_ITINERARY_ENTRY
from itinerary.support import LION_KEY

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.build_itinerary_walk_route import build_itinerary_walk_route
from api.itinerary.routing.itinerary_stop import ENTRANCE_ITEM_KEY
from api.itinerary.routing.order_itinerary_stops_for_walk_route import order_itinerary_stops_for_walk_route
from api.itinerary.routing.resolve_itinerary_stops import resolve_itinerary_stops
from api.itinerary.routing.walk_route_polyline import inclusive_point_slices_for_walk_route_legs
from api.itinerary.routing.walk_route_polyline import walk_route_node_ids_for_point_slice
from api.shared.enums import ScheduleItemKind
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator
from conftest import DbControllers


def _set_rhino_encounter_schedule() -> None:
   assert WildEncounterCoordinator.set_wild_encounter_schedule(
      wild_encounter_name='Guardians of White Rhinos',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='11:00',
      monday=False,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=True,
      sunday=False,
      message=None,
   )


def test_order_itinerary_stops_for_walk_route_returns_empty_without_scheduled_stops(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   ordered_stops = order_itinerary_stops_for_walk_route(
      resolve_itinerary_stops( ItineraryCoordinator.get_itinerary() ) )

   assert ordered_stops == []


def test_order_itinerary_stops_for_walk_route_sorts_scheduled_stops_by_start_time(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_rhino_encounter_schedule()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[ 'Guardians of White Rhinos' ],
      confirming_early_admission=True,
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='14:00',
   ).success

   ordered_stops = order_itinerary_stops_for_walk_route(
      resolve_itinerary_stops( ItineraryCoordinator.get_itinerary() ) )

   assert [ stop.item_key for stop in ordered_stops ] == [
      ENTRANCE_ITEM_KEY,
      'Guardians of White Rhinos',
      LION_KEY,
   ]


def test_build_itinerary_walk_route_returns_empty_path_without_scheduled_stops(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert walk_route.legs == ()
   assert walk_route.points == ()
   assert walk_route.stops == ()


def test_build_itinerary_walk_route_builds_polyline_for_scheduled_animal(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=ANIMAL_KEY,
      start_time='10:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert [ stop.item_key for stop in walk_route.stops ] == [
      ENTRANCE_ITEM_KEY,
      LION_KEY,
   ]
   assert len( walk_route.legs ) == 1
   assert walk_route.legs[ 0 ].from_item_key == ENTRANCE_ITEM_KEY
   assert walk_route.legs[ 0 ].to_item_key == LION_KEY
   assert len( walk_route.legs[ 0 ].node_ids ) >= 2
   assert len( walk_route.points ) == len( walk_route.legs[ 0 ].node_ids )
   assert walk_route.points[ 0 ].node_id == walk_route.legs[ 0 ].node_ids[ 0 ]
   assert walk_route.points[ -1 ].node_id == walk_route.legs[ 0 ].node_ids[ -1 ]
   assert all(
      point.x_px > 0 and point.y_px > 0
      for point in walk_route.points )


CHEETAH_INDO_MALAYA_KEY = 'Cheetah||Indo-Malaya Outdoor'


def test_build_itinerary_walk_route_concatenates_legs_at_shared_node_once(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         LION_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_INDO_MALAYA_KEY,
      start_time='10:00',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='11:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   assert len( walk_route.legs ) == 2
   assert len( walk_route.points ) == (
      len( walk_route.legs[ 0 ].node_ids )
      + len( walk_route.legs[ 1 ].node_ids )
      - 1
   )

   joined_node_id = walk_route.legs[ 0 ].node_ids[ -1 ]

   assert walk_route.legs[ 1 ].node_ids[ 0 ] == joined_node_id
   assert [
      point.node_id
      for point in walk_route.points
   ].count( joined_node_id ) == 1


def test_inclusive_point_slices_for_walk_route_legs_match_polyline(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
         LION_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_INDO_MALAYA_KEY,
      start_time='10:00',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='11:00',
   ).success

   walk_route = build_itinerary_walk_route( ItineraryCoordinator.get_itinerary() )

   for leg, ( from_point_sequence, to_point_sequence ) in zip(
         walk_route.legs,
         inclusive_point_slices_for_walk_route_legs( walk_route.legs ) ):
      assert walk_route_node_ids_for_point_slice(
         walk_route.points,
         from_point_sequence=from_point_sequence,
         to_point_sequence=to_point_sequence ) == leg.node_ids
