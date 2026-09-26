from __future__ import annotations

from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.shared.enums import ItineraryAdjustmentType


def Test_ToDict_TestArrivalAdjustment_ExpectWireShape() -> None:
   previous_value = '9:15 AM'
   value = '09:30'
   adjustment = ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value=previous_value,
      value=value,
      reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS )

   result = adjustment.to_dict()

   assert result[ 'type' ] == adjustment.type.value
   assert result[ 'field' ] == adjustment.field
   assert result[ 'previous_value' ] == adjustment.previous_value
   assert result[ 'value' ] == adjustment.value
   assert result[ 'reason' ] == adjustment.reason.value
