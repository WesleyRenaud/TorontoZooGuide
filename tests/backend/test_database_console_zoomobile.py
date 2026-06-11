from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.zoomobile.coordinators.zoomobile_coordinator import ZoomobileCoordinator
from conftest import DbControllers

def test_set_zoomobile_station_closed_and_open_changes_route_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ZoomobileCoordinator.set_zoomobile_station_as_closed( 'Africa Zoomobile Station', '2026-06-01', '2026-06-30', '' )

   route = ZoomobileCoordinator.get_zoomobile_route( route='summer', day=15, month='June', year=2026 )

   assert all( station.name != 'Africa Zoomobile Station' for station in route.zoomobile_stations )

   assert ZoomobileCoordinator.set_zoomobile_station_as_open( 'Africa Zoomobile Station' )

   route = ZoomobileCoordinator.get_zoomobile_route( route='summer', day=15, month='June', year=2026 )

   assert any( station.name == 'Africa Zoomobile Station' for station in route.zoomobile_stations )

def test_set_current_zoomobile_route_changes_current_route_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ZoomobileCoordinator.set_current_zoomobile_route( 'winter', '2026-06-01', '2026-06-30' )

   route = ZoomobileCoordinator.get_zoomobile_route( route='current', day=15, month='June', year=2026 )

   assert route.route == 'winter'
   assert route.route_source == 'override'
