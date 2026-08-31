from __future__ import annotations

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.warnings.schedule_item_not_on_itinerary_warning_builder import ScheduleItemNotOnItineraryWarningBuilder
from api.shared.enums import ItineraryErrorType


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
   assert ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      AnimalScheduleItemKey( species='African Lion', exhibit='Africa Savanna' ) )


def Test_SavedItineraryHasScheduleItem_TestAnimalWithEnclosure_ExpectTrue() -> None:
   assert ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      AnimalScheduleItemKey(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ) )


def Test_SavedItineraryHasScheduleItem_TestMissingAnimal_ExpectFalse() -> None:
   assert not ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      AnimalScheduleItemKey( species='Cheetah', exhibit='Indo-Malaya Outdoor' ) )


def Test_SavedItineraryHasScheduleItem_TestAttraction_ExpectTrue() -> None:
   assert ScheduleItemNotOnItineraryWarningBuilder.saved_itinerary_has_schedule_item(
      SAVED,
      AttractionScheduleItemKey( name='Conservation Carousel' ) )


def Test_IsRequired_TestConfirming_ExpectFalse(
      stub_no_suppressed_status: None ) -> None:
   assert not ScheduleItemNotOnItineraryWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      SAVED,
      AnimalScheduleItemKey( species='Cheetah', exhibit='Indo-Malaya Outdoor' ),
      confirming_schedule_item_not_on_itinerary=True )


def Test_IsRequired_TestMissingItem_ExpectTrue(
      stub_no_suppressed_status: None ) -> None:
   assert ScheduleItemNotOnItineraryWarningBuilder.is_required(
      object(),  # type: ignore[arg-type]
      SAVED,
      AnimalScheduleItemKey( species='Cheetah', exhibit='Indo-Malaya Outdoor' ),
      confirming_schedule_item_not_on_itinerary=False )
