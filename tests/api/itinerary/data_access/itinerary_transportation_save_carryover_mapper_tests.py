from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_transportation_save_carryover_mapper import ItineraryTransportationSaveCarryoverMapper
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg


ZOOMOBILE = 'Zoomobile'


def _leg() -> ItineraryTransportationLeg:
   return ItineraryTransportationLeg(
      from_station='Africa',
      to_station='Americas',
      start_time='11:00 AM',
      end_time='11:10 AM',
      transportation=ZOOMOBILE,
      added_as_attraction=True )


def Test_MapFromSavedTransportationRows_TestMatchingMode_ExpectScheduleAndLegs() -> None:
   carryover = ItineraryTransportationSaveCarryoverMapper.map_from_saved_transportation_rows(
      [
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=True,
            start_time='11:00 AM',
            end_time='11:20 AM',
            bulk_transit_evaluated=True,
            legs=[ _leg() ],
         ),
      ],
      ItineraryTransportationInput( name=ZOOMOBILE, added_as_attraction=True ),
      old_visit_date='2026-06-15',
   )

   assert carryover.start_time == '11:00 AM'
   assert carryover.end_time == '11:20 AM'
   assert carryover.bulk_transit_evaluated is True
   assert len( carryover.legs ) == 1


def Test_MapFromSavedTransportationRows_TestModeMismatch_ExpectEmptyCarryover() -> None:
   carryover = ItineraryTransportationSaveCarryoverMapper.map_from_saved_transportation_rows(
      [
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=True,
            start_time='11:00 AM',
            end_time='11:20 AM',
         ),
      ],
      ItineraryTransportationInput( name=ZOOMOBILE, added_as_attraction=False ),
      old_visit_date='2026-06-15',
   )

   assert carryover.start_time is None
   assert carryover.end_time is None
   assert carryover.legs == []
