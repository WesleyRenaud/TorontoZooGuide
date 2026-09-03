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

   assert diff.to_dict() == {
      'name': 'Zoomobile',
      'old_likelihood': 90,
      'new_likelihood': 70,
      'start_time': '10:00 AM',
      'end_time': '10:20 AM',
      'legs': [ leg.to_dict() ],
      'route': 'summer',
      'route_marker_sequences': [ [ 'zm-s-001' ] ],
      'added_as_attraction': True,
      'bulk_transit_evaluated': True,
   }
