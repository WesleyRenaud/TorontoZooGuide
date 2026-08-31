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
      from_station='Main Zoomobile Station',
      to_station='Africa Zoomobile Station',
      start_time='11:00 AM',
      end_time='11:20 AM',
      transportation='Zoomobile',
      added_as_attraction=False )


def Test_Build_TestWithLegs_ExpectMainStationCoords() -> None:
   assert ItineraryTransportationMarkerCoordsBuilder.build(
      [ _leg() ],
      ATTRACTION_COORDS,
      MAIN_STATION ) == ( 10.0, 20.0 )


def Test_Build_TestNoLegsAndNoAttractionCoords_ExpectMainStationCoords() -> None:
   assert ItineraryTransportationMarkerCoordsBuilder.build(
      [],
      None,
      MAIN_STATION ) == ( 10.0, 20.0 )


def Test_Build_TestNoLegsWithAttractionCoords_ExpectAttractionCoords() -> None:
   assert ItineraryTransportationMarkerCoordsBuilder.build(
      [],
      ATTRACTION_COORDS,
      MAIN_STATION ) == ATTRACTION_COORDS
