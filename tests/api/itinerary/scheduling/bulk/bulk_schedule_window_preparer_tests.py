from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.bulk.bulk_schedule_window_preparer import BulkScheduleWindowPreparer


EMPTY_SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-20',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
)

SAVED_ITINERARY_WITH_TALK = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   guardians_talk_rows=[
      ItineraryGuardiansTalkRecord(
         talk_name="Grevy's Zebra",
         start_time='2:00 PM',
         end_time='2:30 PM',
         is_deleted=False,
      ),
   ],
)


def Test_HasItemsToRebuild_TestEmptyGuestItems_ExpectFalse() -> None:
   assert not BulkScheduleWindowPreparer.has_items_to_rebuild( EMPTY_SAVED_ITINERARY )


def Test_HasItemsToRebuild_TestGuardiansTalkOnly_ExpectTrue() -> None:
   assert BulkScheduleWindowPreparer.has_items_to_rebuild( SAVED_ITINERARY_WITH_TALK )


def Test_HasItemsToRebuild_TestAnimalRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


def Test_HasItemsToRebuild_TestAttractionRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      attraction_rows=[
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


def Test_HasItemsToRebuild_TestTransportationRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=[
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=None,
            added_as_attraction=False,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )


def Test_HasItemsToRebuild_TestWildEncounterRow_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=[
         ItineraryWildEncounterRecord(
            wild_encounter='Grizzly Bear',
            start_time='2:00 PM',
            end_time='2:45 PM',
            is_deleted=False,
         ),
      ],
   )

   assert BulkScheduleWindowPreparer.has_items_to_rebuild( saved )
