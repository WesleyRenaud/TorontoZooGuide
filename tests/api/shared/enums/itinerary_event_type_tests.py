from __future__ import annotations

from api.shared.enums.itinerary_event_type import ItineraryEventType


def Test_Normalize_TestLunchValue_ExpectLunchType() -> None:
   value = ItineraryEventType.LUNCH.value

   event_type = ItineraryEventType.normalize( value )

   assert event_type == ItineraryEventType.LUNCH


def Test_Normalize_TestArrivalWhitespace_ExpectArrivalType() -> None:
   value = f' { ItineraryEventType.ARRIVAL.value.upper() } '

   event_type = ItineraryEventType.normalize( value )

   assert event_type == ItineraryEventType.ARRIVAL


def Test_Normalize_TestNone_ExpectNone() -> None:
   value = None

   event_type = ItineraryEventType.normalize( value )

   assert event_type is None


def Test_Normalize_TestUnknown_ExpectNone() -> None:
   value = 'snooze'

   event_type = ItineraryEventType.normalize( value )

   assert event_type is None
