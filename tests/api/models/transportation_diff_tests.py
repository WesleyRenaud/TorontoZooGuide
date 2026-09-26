from __future__ import annotations

from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.models.transportation_diff import TransportationDiff


def Test_ToDict_TestLegsAndFlags_ExpectFrontendShape() -> None:
   leg = ItineraryTransportationLeg(
      transportation='Zoomobile',
      from_station='Main Zoomobile Station',
      to_station='Eurasia Zoomobile Station',
      start_time='10:00 AM',
      end_time='10:20 AM',
      added_as_attraction=False )
   diff = TransportationDiff(
      name='Zoomobile',
      old_likelihood=90,
      new_likelihood=70,
      start_time='10:00 AM',
      end_time='10:20 AM',
      legs=[ leg ],
      route='summer',
      route_marker_sequences=[ [ 'zm-s-001' ] ],
      added_as_attraction=True,
      bulk_transit_evaluated=True )

   result = diff.to_dict()

   assert result[ 'name' ] == diff.name
   assert result[ 'old_likelihood' ] == diff.old_likelihood
   assert result[ 'new_likelihood' ] == diff.new_likelihood
   assert result[ 'start_time' ] == diff.start_time
   assert result[ 'end_time' ] == diff.end_time
   assert result[ 'legs' ] == [ transportation_leg.to_dict() for transportation_leg in diff.legs ]
   assert result[ 'route' ] == diff.route
   assert result[ 'route_marker_sequences' ] == diff.route_marker_sequences
   assert result[ 'added_as_attraction' ] is diff.added_as_attraction
   assert result[ 'bulk_transit_evaluated' ] is diff.bulk_transit_evaluated
