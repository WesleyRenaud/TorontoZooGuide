from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.transportation.coordinators.transportation_coordinator import TransportationCoordinator
from conftest import DbControllers

def test_transportation_route_selection_and_station_filtering(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 1, 15 ) )

   manual = TransportationCoordinator.get_transportation_route( route='winter', day=15, month='January', year=2026 )
   invalid = TransportationCoordinator.get_transportation_route( route='bad-route', day=15, month='January', year=2026 )

   assert manual.route == 'winter'
   assert invalid.route == 'summer'

   assert TransportationCoordinator.set_current_transportation_route( route='winter', start_date='2026-01-01', end_date='2026-01-31' )
   current = TransportationCoordinator.get_transportation_route( route='current', day=15, month='January', year=2026 )

   assert current.route == 'winter'
   assert current.route_source == 'override'
   assert all( station.name != 'Africa Zoomobile Station' for station in current.transportation_stations )
