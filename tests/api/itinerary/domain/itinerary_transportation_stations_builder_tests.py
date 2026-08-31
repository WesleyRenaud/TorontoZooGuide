from __future__ import annotations

from api.itinerary.domain.itinerary_transportation_stations_builder import ItineraryTransportationStationsBuilder
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg


def _leg(
      *,
      from_station: str,
      to_station: str,
      start_time: str,
      end_time: str ) -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station=from_station,
      to_station=to_station,
      start_time=start_time,
      end_time=end_time,
      transportation='Zoomobile',
      added_as_attraction=False )


def Test_GroupConsecutiveLegSequences_TestContinuousLegs_ExpectOneSequence() -> None:
   legs = [
      _leg(
         from_station='Africa',
         to_station='Americas',
         start_time='10:00 AM',
         end_time='10:10 AM' ),
      _leg(
         from_station='Americas',
         to_station='Eurasia',
         start_time='10:10 AM',
         end_time='10:20 AM' ),
   ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert len( sequences ) == 1
   assert [ ( leg.from_station, leg.to_station ) for leg in sequences[ 0 ] ] == [
      ( 'Africa', 'Americas' ),
      ( 'Americas', 'Eurasia' ),
   ]


def Test_GroupConsecutiveLegSequences_TestStationOrTimeGap_ExpectSplitSequences() -> None:
   legs = [
      _leg(
         from_station='Africa',
         to_station='Americas',
         start_time='10:00 AM',
         end_time='10:10 AM' ),
      _leg(
         from_station='Eurasia',
         to_station='Indo-Malaya',
         start_time='10:10 AM',
         end_time='10:20 AM' ),
      _leg(
         from_station='Indo-Malaya',
         to_station='Canadian Domain',
         start_time='11:00 AM',
         end_time='11:10 AM' ),
   ]

   sequences = ItineraryTransportationStationsBuilder.group_consecutive_leg_sequences( legs )

   assert [
      [ ( leg.from_station, leg.to_station ) for leg in sequence ]
      for sequence in sequences
   ] == [
      [ ( 'Africa', 'Americas' ) ],
      [ ( 'Eurasia', 'Indo-Malaya' ) ],
      [ ( 'Indo-Malaya', 'Canadian Domain' ) ],
   ]
