from __future__ import annotations

from api.guardians.scheduling.guardians_talk_loop_schedule_pin import resolve_guardians_talk_loop_pin
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.models import GuardiansTalk
from api.shared.enums import ScheduleItemKind
from api.walk_graph.master_route import default_master_route_loop_by_id
from conftest import DbControllers


def test_resolve_guardians_talk_loop_pin_returns_none_for_unmapped_talk(
      db: DbControllers ) -> None:
   guardians_talk = GuardiansTalk(
      name='Not On Master Route',
      location='Nowhere',
      x_coord=0.0,
      y_coord=0.0,
      start_time='10:00 AM',
      end_time='10:30 AM' )
   itinerary_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='Not On Master Route',
      walk_node_ids=( 'v-1061', ),
      is_fixed_time=True,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   assert resolve_guardians_talk_loop_pin(
      db.conn,
      guardians_talk,
      itinerary_stop ) is None


def test_resolve_guardians_talk_loop_pin_returns_pin_for_african_lion(
      db: DbControllers ) -> None:
   guardians_talk = GuardiansTalk(
      name='African Lion',
      location='Africa Savanna',
      x_coord=51.138,
      y_coord=41.279,
      start_time='10:00 AM',
      end_time='10:30 AM' )
   itinerary_stop = ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key='African Lion',
      walk_node_ids=( 'v-0436', ),
      is_fixed_time=True,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   loop_pin = resolve_guardians_talk_loop_pin(
      db.conn,
      guardians_talk,
      itinerary_stop )

   assert loop_pin is not None
   assert loop_pin.loop_id == 'africa_savanna_canadian_domain'
   assert loop_pin.viewing_spot_index == viewing_spot_index_for_african_lion()


def viewing_spot_index_for_african_lion() -> int:
   master_route_loop = default_master_route_loop_by_id()[ 'africa_savanna_canadian_domain' ]

   for index, viewing_spot in enumerate( master_route_loop.viewing_spots ):
      if (
            viewing_spot.species == 'African Lion'
            and viewing_spot.exhibit == 'Africa Savanna' ):
         return index

   raise AssertionError( 'African Lion viewing spot not found in savanna loop' )
