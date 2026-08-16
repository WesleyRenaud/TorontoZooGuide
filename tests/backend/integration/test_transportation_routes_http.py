from __future__ import annotations

from pathlib import Path

from http_client import post_route


def test_get_transportations_returns_attraction_marker_data(
      integration_db: Path,
) -> None:
   status, response = post_route( '/get-transportations', {} )

   assert status == 200
   assert response[ 'transportations' ] == [
      {
         'name': 'Zoomobile',
         'is_also_attraction': True,
         'free_with_admission': False,
         'description': 'All Aboard for a Wild Ride! Climb aboard the Zoomobile for a fun ride through your Toronto Zoo!',
         'info_link': 'https://www.torontozoo.com/tickets/zoomobile',
         'hyperlink_text': 'PRICING & DETAILS',
         'x_coord': 56.068,
         'y_coord': 83.343,
         'region': 'Front Courtyard',
      },
   ]


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
