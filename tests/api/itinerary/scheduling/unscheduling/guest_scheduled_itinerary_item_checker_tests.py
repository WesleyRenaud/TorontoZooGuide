from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.unscheduling.guest_scheduled_itinerary_item_checker import GuestScheduledItineraryItemChecker
from api.shared.enums import ItineraryEventType


VISIT_DATE = '2026-06-15'
ARRIVAL_TIME = '9:30 AM'
DEPARTURE_TIME = '5:00 PM'


def Test_HasItems_TestScheduledAnimal_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )

   has_items = GuestScheduledItineraryItemChecker.has_items( saved )

   assert has_items


def Test_HasItems_TestEventRowsOnly_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      event_rows=[
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
      ],
   )

   has_items = GuestScheduledItineraryItemChecker.has_items( saved )

   assert has_items


def Test_HasItems_TestUnscheduledOnly_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
   )

   has_items = GuestScheduledItineraryItemChecker.has_items( saved )

   assert not has_items


def Test_HasItems_TestScheduledAttraction_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=100,
            start_time='11:00 AM',
            end_time='11:20 AM' ),
      ],
   )

   has_items = GuestScheduledItineraryItemChecker.has_items( saved )

   assert has_items


def Test_HasItems_TestScheduledTransportation_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=100,
            added_as_attraction=True,
            start_time='11:00 AM',
            end_time='11:20 AM' ),
      ],
   )

   has_items = GuestScheduledItineraryItemChecker.has_items( saved )

   assert has_items


def Test_HasItems_TestGuardiansTalkOnly_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value=VISIT_DATE,
      arrival_time=ARRIVAL_TIME,
      departure_time=DEPARTURE_TIME,
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name='African Lion',
            start_time='2:00 PM',
            end_time='2:30 PM',
            is_deleted=False ),
      ],
   )

   has_items = GuestScheduledItineraryItemChecker.has_items( saved )

   assert not has_items
