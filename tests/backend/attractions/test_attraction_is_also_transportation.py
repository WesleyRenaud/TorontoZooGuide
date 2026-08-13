from __future__ import annotations

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from conftest import DbControllers


def test_zoomobile_is_seeded_as_also_transportation( db: DbControllers ) -> None:
   attractions = AttractionCoordinator.get_attractions(
      day=15,
      month='June',
      year=2026,
      include_closed_attractions=True )
   by_name = {
      attraction.name: attraction
      for attraction in attractions
   }

   assert by_name[ 'Zoomobile' ].is_also_transportation is True
   assert by_name[ 'Conservation Carousel' ].is_also_transportation is False
   assert by_name[ 'Zoomobile' ].to_dict()[ 'is_also_transportation' ] is True
