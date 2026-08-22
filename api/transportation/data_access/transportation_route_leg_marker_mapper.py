from __future__ import annotations

from collections import defaultdict

from .transportation_route_leg_marker_record import TransportationRouteLegMarkerRecord
from ...types import Row


def map_transportation_route_leg_marker(
      row: Row,
) -> TransportationRouteLegMarkerRecord:
   return TransportationRouteLegMarkerRecord(
      from_station=row[ 'FROM_STATION' ],
      to_station=row[ 'TO_STATION' ],
      marker_id=row[ 'MARKER_ID' ],
   )


def map_transportation_route_leg_markers(
      rows: list[ Row ],
) -> list[ TransportationRouteLegMarkerRecord ]:
   return [
      map_transportation_route_leg_marker( row )
      for row in rows
   ]


def markers_by_leg_for_markers(
      markers: list[ TransportationRouteLegMarkerRecord ],
) -> dict[ tuple[ str, str ], list[ str ] ]:
   markers_by_leg: dict[ tuple[ str, str ], list[ str ] ] = defaultdict( list )

   for marker in markers:
      markers_by_leg[ ( marker.from_station, marker.to_station ) ].append(
         marker.marker_id )

   return dict( markers_by_leg )
