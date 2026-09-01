from __future__ import annotations

import pytest

from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from api.guardians.data_access.guardians_talk_animal_record import GuardiansTalkAnimalRecord
from api.guardians.scheduling.guardians_talk_loop_schedule_pin_resolver import GuardiansTalkLoopSchedulePinResolver
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.models import GuardiansTalk
from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.master_route_loop import MasterRouteLoop
from api.walk_graph.domain.master_route_loop import ONE_WAY_LOOP_TRAVERSAL
from api.walk_graph.domain.viewing_spot_reference import ViewingSpotReference
from api.walk_graph.master_route_provider import MasterRouteProvider


AFRICA_LOOP = MasterRouteLoop(
   loop_id='africa_savanna_canadian_domain',
   name='Africa Savanna',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      ViewingSpotReference(
         species='African Lion',
         exhibit='Africa Savanna',
         name=None ),
      ViewingSpotReference(
         species='African Penguin',
         exhibit='Africa Savanna',
         name='Outdoor' ),
      ViewingSpotReference(
         species='African Penguin',
         exhibit='Africa Savanna',
         name='Indoor' ),
   ],
)

RAINFOREST_LOOP = MasterRouteLoop(
   loop_id='african_rainforest_giraffe',
   name='African Rainforest',
   traversal=ONE_WAY_LOOP_TRAVERSAL,
   viewing_spots=[
      ViewingSpotReference(
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         name='Indoor' ),
   ],
)

LOOPS_BY_ID = {
   'africa_savanna_canadian_domain': AFRICA_LOOP,
   'african_rainforest_giraffe': RAINFOREST_LOOP,
}

ANIMAL_LINKS_BY_TALK = {
   'African Penguin': [
      GuardiansTalkAnimalRecord(
         talk_name='African Penguin',
         location='Africa Savanna',
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
      ),
   ],
   'Western Lowland Gorilla': [
      GuardiansTalkAnimalRecord(
         talk_name='Western Lowland Gorilla',
         location='African Rainforest Pavilion',
         species='Western Lowland Gorilla',
         exhibit='African Rainforest Pavilion',
         enclosure_name='Indoor',
      ),
   ],
   'African Lion': [
      GuardiansTalkAnimalRecord(
         talk_name='African Lion',
         location='Africa Savanna',
         species='African Lion',
         exhibit='Africa Savanna',
      ),
   ],
}


def _itinerary_stop( *, item_key: str ) -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key=item_key,
      walk_node_ids=( 'v-0436', ),
      is_fixed_time=True,
      start_time='10:00 AM',
      end_time='10:30 AM' )


@pytest.fixture
def stub_guardians_talk_loop_schedule_pin_resolver(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      MasterRouteProvider,
      'loops_by_id',
      lambda: LOOPS_BY_ID )
   monkeypatch.setattr(
      GuardiansTalkAnimalProvider,
      'fetch_animal_links',
      lambda conn, talk_name: ANIMAL_LINKS_BY_TALK.get( talk_name, [] ) )


def Test_Resolve_TestUnmappedTalk_ExpectNone(
      stub_guardians_talk_loop_schedule_pin_resolver: None ) -> None:
   guardians_talk = GuardiansTalk(
      name='Not On Master Route',
      location='Nowhere',
      x_coord=0.0,
      y_coord=0.0,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   assert GuardiansTalkLoopSchedulePinResolver.resolve(
      None,
      guardians_talk,
      _itinerary_stop( item_key='Not On Master Route' ) ) is None


def Test_Resolve_TestAfricanLionTalk_ExpectSavannaLoopPin(
      stub_guardians_talk_loop_schedule_pin_resolver: None ) -> None:
   guardians_talk = GuardiansTalk(
      name='African Lion',
      location='Africa Savanna',
      x_coord=51.138,
      y_coord=41.279,
      start_time='10:00 AM',
      end_time='10:30 AM' )

   loop_pin = GuardiansTalkLoopSchedulePinResolver.resolve(
      None,
      guardians_talk,
      _itinerary_stop( item_key='African Lion' ) )

   assert loop_pin is not None
   assert loop_pin.loop_id == 'africa_savanna_canadian_domain'
   assert loop_pin.viewing_spot_index == 0


def Test_Resolve_TestPenguinTalk_ExpectOutdoorEnclosurePin(
      stub_guardians_talk_loop_schedule_pin_resolver: None ) -> None:
   loop_pin = GuardiansTalkLoopSchedulePinResolver.resolve(
      None,
      GuardiansTalk(
         name='African Penguin',
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='11:00 AM',
         end_time='11:30 AM',
      ),
      _itinerary_stop( item_key='African Penguin' ) )

   assert loop_pin is not None
   assert loop_pin.loop_id == 'africa_savanna_canadian_domain'
   assert loop_pin.viewing_spot_index == 1


def Test_Resolve_TestGorillaTalk_ExpectIndoorEnclosurePin(
      stub_guardians_talk_loop_schedule_pin_resolver: None ) -> None:
   loop_pin = GuardiansTalkLoopSchedulePinResolver.resolve(
      None,
      GuardiansTalk(
         name='Western Lowland Gorilla',
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='11:00 AM',
         end_time='11:30 AM',
      ),
      _itinerary_stop( item_key='Western Lowland Gorilla' ) )

   assert loop_pin is not None
   assert loop_pin.loop_id == 'african_rainforest_giraffe'
   assert loop_pin.viewing_spot_index == 0


def Test_Resolve_TestLionTalk_ExpectNullEnclosurePin(
      stub_guardians_talk_loop_schedule_pin_resolver: None ) -> None:
   loop_pin = GuardiansTalkLoopSchedulePinResolver.resolve(
      None,
      GuardiansTalk(
         name='African Lion',
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='11:00 AM',
         end_time='11:30 AM',
      ),
      _itinerary_stop( item_key='African Lion' ) )

   assert loop_pin is not None
   assert loop_pin.viewing_spot_index == 0
