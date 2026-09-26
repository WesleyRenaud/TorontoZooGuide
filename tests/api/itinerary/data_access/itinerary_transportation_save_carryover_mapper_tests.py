from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_transportation_save_carryover_mapper import ItineraryTransportationSaveCarryoverMapper
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.date_values import DateValues
from api.shared.enums.position import Position
from api.shared.enums.transportation_name import TransportationName


def Test_MapFromSavedTransportationRows_TestMatchingMode_ExpectScheduleAndLegs() -> None:
   transportation = TransportationName.ZOOMOBILE
   added_as_attraction = True
   start_time = '11:00 AM'
   duration_minutes = 20
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   leg_duration_minutes = 10
   legs = [
      ItineraryTransportationLeg(
         from_station='Africa',
         to_station='Americas',
         start_time=start_time,
         end_time=DateValues.add_minutes_to_time( start_time, leg_duration_minutes ),
         transportation=transportation,
         added_as_attraction=added_as_attraction ),
   ]
   saved_rows = [
      ItineraryTransportationRecord(
         transportation=transportation,
         old_likelihood=None,
         new_likelihood=100,
         added_as_attraction=added_as_attraction,
         start_time=start_time,
         end_time=end_time,
         bulk_transit_evaluated=True,
         legs=legs ),
   ]
   transportation_input = ItineraryTransportationInput(
      name=transportation,
      added_as_attraction=added_as_attraction )
   old_visit_date = '2026-06-15'

   carryover = ItineraryTransportationSaveCarryoverMapper.map_from_saved_transportation_rows(
      saved_rows,
      transportation_input,
      old_visit_date=old_visit_date )

   saved_row = saved_rows[ Position.FIRST ]
   assert carryover.start_time == saved_row.start_time
   assert carryover.end_time == saved_row.end_time
   assert carryover.bulk_transit_evaluated is saved_row.bulk_transit_evaluated
   assert len( carryover.legs ) == len( saved_row.legs )


def Test_MapFromSavedTransportationRows_TestModeMismatch_ExpectEmptyCarryover() -> None:
   transportation = TransportationName.ZOOMOBILE
   start_time = '11:00 AM'
   duration_minutes = 20
   saved_rows = [
      ItineraryTransportationRecord(
         transportation=transportation,
         old_likelihood=None,
         new_likelihood=100,
         added_as_attraction=True,
         start_time=start_time,
         end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) ),
   ]
   transportation_input = ItineraryTransportationInput(
      name=transportation,
      added_as_attraction=False )
   old_visit_date = '2026-06-15'

   carryover = ItineraryTransportationSaveCarryoverMapper.map_from_saved_transportation_rows(
      saved_rows,
      transportation_input,
      old_visit_date=old_visit_date )

   assert carryover.start_time is None
   assert carryover.end_time is None
   assert carryover.legs == []
