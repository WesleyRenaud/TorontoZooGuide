from __future__ import annotations

from api.shared.enums.itinerary_event_type import ItineraryEventType

def Test_Normalize_TestCanonicalValue_ExpectMatchingType() -> None:
   assert ItineraryEventType.normalize( 'lunch' ) == ItineraryEventType.LUNCH
   assert ItineraryEventType.normalize( ' ARRIVAL ' ) == ItineraryEventType.ARRIVAL

def Test_Normalize_TestNoneOrUnknown_ExpectNone() -> None:
   assert ItineraryEventType.normalize( None ) is None
   assert ItineraryEventType.normalize( 'snooze' ) is None
