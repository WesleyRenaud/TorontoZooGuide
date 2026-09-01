from __future__ import annotations

from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.domain.itinerary_adjustment_type import ItineraryAdjustmentType


ARRIVAL_ADJUSTMENT = ItineraryAdjustment(
   type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
   field='arrivalTime',
   previous_value='9:15 AM',
   value='09:30',
   reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS,
)


def Test_ToDict_TestArrivalAdjustment_ExpectWireShape() -> None:
   assert ARRIVAL_ADJUSTMENT.to_dict() == {
      'type': 'arrivalTimeAdjusted',
      'field': 'arrivalTime',
      'previous_value': '9:15 AM',
      'value': '09:30',
      'reason': 'arrivalOutsideAdmissionHours',
   }
