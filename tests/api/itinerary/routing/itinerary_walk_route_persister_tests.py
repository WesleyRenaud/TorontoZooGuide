from __future__ import annotations

import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.data_access.itinerary_walk_route_provider import ItineraryWalkRouteProvider
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.routing.itinerary_walk_route import ItineraryWalkRoute
from api.itinerary.routing.itinerary_walk_route_builder import ItineraryWalkRouteBuilder
from api.itinerary.routing.itinerary_walk_route_persister import ItineraryWalkRoutePersister
from api.itinerary.routing.itinerary_walk_route_stop import ItineraryWalkRouteStop
from api.itinerary.routing.walk_route_point import WalkRoutePoint
from api.itinerary.scheduling.items.itinerary_schedule_context_builder import ItineraryScheduleContextBuilder
from api.models import Itinerary
from api.shared.enums import ScheduleItemKind
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


BUILT_ROUTE = ItineraryWalkRoute(
   stops=[
      ItineraryWalkRouteStop(
         schedule_item_kind=ScheduleItemKind.ENTRANCE,
         item_key='entrance',
         walk_node_id='n-1' ),
   ],
   legs=[],
   points=[
      WalkRoutePoint(
         node_id='n-1',
         x=0.0,
         y=0.0,
         x_px=0.0,
         y_px=0.0 ),
   ] )

SAVED_ITINERARY = object()
SCHEDULE_CONTEXT = { 'visit_date_temp': 20.0 }
CURRENT_ITINERARY = ItineraryBuilder.build(
   date='2026-06-20',
   selected_exhibits=[],
   animals=[],
   attractions=[],
   transportations=[],
   transportation_stations=[],
   guardians_talks=[],
   wild_encounters=[],
   events=[],
   arrival_time='9:30 AM',
   departure_time='5:00 PM' )


@pytest.fixture
def stub_itinerary_walk_route_persister_dependencies(
      monkeypatch: pytest.MonkeyPatch ) -> list[ ItineraryWalkRoute ]:
   saved_routes: list[ ItineraryWalkRoute ] = []

   monkeypatch.setattr(
      ItineraryScheduleContextBuilder,
      'build',
      lambda **kwargs: SCHEDULE_CONTEXT )
   monkeypatch.setattr(
      ItineraryProvider,
      'fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItineraryBuilder,
      'build_current',
      lambda saved_itinerary, **context: CURRENT_ITINERARY )
   monkeypatch.setattr(
      ItineraryWalkRouteBuilder,
      'build',
      lambda itinerary: BUILT_ROUTE )
   monkeypatch.setattr(
      ItineraryWalkRouteProvider,
      'save_itinerary_walk_route',
      lambda conn, walk_route: saved_routes.append( walk_route ) or True )

   return saved_routes


def Test_RebuildAndPersist_TestSavedItinerary_ExpectBuiltRoutePersisted(
      stub_itinerary_walk_route_persister_dependencies: list[ ItineraryWalkRoute ] ) -> None:
   conn = sqlite3.connect( ':memory:' )

   try:
      assert ItineraryWalkRoutePersister.rebuild_and_persist(
         conn,
         animal_coordinator=AnimalCoordinator,
         attraction_coordinator=AttractionCoordinator,
         guardians_coordinator=GuardiansCoordinator,
         wild_encounter_coordinator=WildEncounterCoordinator )
      assert stub_itinerary_walk_route_persister_dependencies == [ BUILT_ROUTE ]
   finally:
      conn.close()
