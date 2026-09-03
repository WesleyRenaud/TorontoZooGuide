from __future__ import annotations

from api.models.itinerary_transportation import ItineraryTransportation
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.models.itinerary_transportation_station import ItineraryTransportationStation
from api.shared.enums.itinerary_transportation_station_role import ItineraryTransportationStationRole

def Test_ToDict_TestZoomobile_ExpectSerializedFields() -> None:
   transportation = ItineraryTransportation(
      name='Zoomobile',
      added_as_attraction=True,
      old_likelihood=1,
      likelihood=3,
      start_time='11:00 AM',
      end_time='11:30 AM',
      legs=[
         ItineraryTransportationLeg(
            transportation='Zoomobile',
            added_as_attraction=False,
            from_station='Main',
            to_station='Canada',
            start_time='11:30 AM',
            end_time='11:45 AM' ),
      ],
      stations=[
         ItineraryTransportationStation(
            name='Main',
            transportation='Zoomobile',
            role=ItineraryTransportationStationRole.ONBOARDING,
            description='Main station',
            x_coord=1.0,
            y_coord=2.0 ),
      ],
      route='route-a',
      bulk_transit_evaluated=True )

   result = transportation.to_dict()

   assert result[ 'name' ] == 'Zoomobile'
   assert result[ 'added_as_attraction' ] is True
   assert result[ 'bulk_transit_evaluated' ] is True
   assert len( result[ 'legs' ] ) == 1
   assert len( result[ 'stations' ] ) == 1
