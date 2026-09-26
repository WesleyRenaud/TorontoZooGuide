from __future__ import annotations

from api_test_support.request_connection_test_support import STUB_REQUEST_CONNECTION
import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.warnings.schedule_item_not_on_itinerary_warning_builder import ScheduleItemNotOnItineraryWarningBuilder
from api.shared.enums import ItineraryErrorType, Position


SAVED = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100 ),
      ItineraryAnimalRecord(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         old_likelihood=None,
         new_likelihood=100 ),
   ],
   attraction_rows=[
      ItineraryAttractionRecord(
         attraction='Conservation Carousel',
         old_likelihood=None,
         new_likelihood=100 ),
   ],
)


@pytest.fixture
def stub_no_suppressed_status( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, _error_type: False )


def Test_SavedItineraryHasScheduleItem_TestAnimalWithoutEnclosure_ExpectTrue() -> None:
   lion = SAVED.animal_rows[ Position.FIRST ]
   key = AnimalScheduleItemKey( species=lion.species, exhibit=lion.exhibit )

   found = ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      key )

   assert found is True


def Test_SavedItineraryHasScheduleItem_TestAnimalWithEnclosure_ExpectTrue() -> None:
   penguin = SAVED.animal_rows[ Position.SECOND ]
   key = AnimalScheduleItemKey(
      species=penguin.species,
      exhibit=penguin.exhibit,
      enclosure_name=penguin.enclosure_name )

   found = ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      key )

   assert found is True


def Test_SavedItineraryHasScheduleItem_TestMissingAnimal_ExpectFalse() -> None:
   key = AnimalScheduleItemKey( species='Cheetah', exhibit='Indo-Malaya Outdoor' )

   found = ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      key )

   assert found is False


def Test_SavedItineraryHasScheduleItem_TestAttraction_ExpectTrue() -> None:
   attraction = SAVED.attraction_rows[ Position.FIRST ]
   key = AttractionScheduleItemKey( name=attraction.attraction )

   found = ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      key )

   assert found is True


def Test_IsRequired_TestConfirming_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   key = AnimalScheduleItemKey( species='Cheetah', exhibit='Indo-Malaya Outdoor' )
   confirming_schedule_item_not_on_itinerary = True

   required = ScheduleItemNotOnItineraryWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      SAVED,
      key,
      confirming_schedule_item_not_on_itinerary=confirming_schedule_item_not_on_itinerary )

   assert required is False


def Test_IsRequired_TestMissingItem_ExpectTrue(
      stub_no_suppressed_status: None ) -> None:
   key = AnimalScheduleItemKey( species='Cheetah', exhibit='Indo-Malaya Outdoor' )
   confirming_schedule_item_not_on_itinerary = False

   required = ScheduleItemNotOnItineraryWarningBuilder.is_required(
      STUB_REQUEST_CONNECTION,
      SAVED,
      key,
      confirming_schedule_item_not_on_itinerary=confirming_schedule_item_not_on_itinerary )

   assert required is True
