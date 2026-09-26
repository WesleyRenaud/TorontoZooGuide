from __future__ import annotations

from api.itinerary.domain.itinerary_transportation_marker_coords_builder import ItineraryTransportationMarkerCoordsBuilder
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.transportation.data_access.transportation_station_record import TransportationStationRecord


MAIN_STATION = TransportationStationRecord(
   name='Main Zoomobile Station',
   description='Main',
   x_coord=10.0,
   y_coord=20.0,
)

ATTRACTION_COORDS = ( 30.0, 40.0 )


def _leg() -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=MAIN_STATION.name,
      to_station='Africa Zoomobile Station',
      start_time='11:00 AM',
      end_time='11:20 AM',
      transportation='Zoomobile',
      added_as_attraction=False )


def Test_Build_TestWithLegs_ExpectMainStationCoords() -> None:
   legs = [ _leg() ]

   coords = ItineraryTransportationMarkerCoordsBuilder.build(
      legs,
      ATTRACTION_COORDS,
      MAIN_STATION )

   assert coords == ( MAIN_STATION.x_coord, MAIN_STATION.y_coord )


def Test_Build_TestNoLegsAndNoAttractionCoords_ExpectMainStationCoords() -> None:
   attraction_coords = None

   coords = ItineraryTransportationMarkerCoordsBuilder.build(
      [],
      attraction_coords,
      MAIN_STATION )

   assert coords == ( MAIN_STATION.x_coord, MAIN_STATION.y_coord )


def Test_Build_TestNoLegsWithAttractionCoords_ExpectAttractionCoords() -> None:
   coords = ItineraryTransportationMarkerCoordsBuilder.build(
      [],
      ATTRACTION_COORDS,
      MAIN_STATION )

   assert coords == ATTRACTION_COORDS
