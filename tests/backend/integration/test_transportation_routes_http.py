from __future__ import annotations

from pathlib import Path

from http_client import post_route


def test_get_transportation_routes_returns_seeded_routes(
      integration_db: Path,
) -> None:
   status, response = post_route( '/get-transportation-routes', {} )

   assert status == 200
   assert response[ 'transportations' ] == [
      {
         'name': 'Zoomobile',
         'routes': [ 'summer', 'winter' ],
      },
   ]
