from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_animal_save_carryover_mapper import ItineraryAnimalSaveCarryoverMapper


def Test_MapFromSavedAnimalRows_TestMatchingSpeciesExhibit_ExpectScheduleCarryover() -> None:
   carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='2:30 PM',
            end_time='2:45 PM',
         ),
      ],
      ItineraryAnimalInput(
         species='African Lion',
         exhibit='Africa Savanna' ),
      old_visit_date='2026-06-15',
   )

   assert carryover.start_time == '2:30 PM'
   assert carryover.end_time == '2:45 PM'


def Test_MapFromSavedAnimalRows_TestNoOldVisitDate_ExpectEmptyCarryover() -> None:
   carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
      [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='2:30 PM',
            end_time='2:45 PM',
         ),
      ],
      ItineraryAnimalInput(
         species='African Lion',
         exhibit='Africa Savanna' ),
      old_visit_date=None,
   )

   assert carryover.start_time is None
   assert carryover.end_time is None
   assert carryover.added_by_transportation is False


def Test_MapFromSavedAnimalRows_TestTransportationOwnedSavedRow_ExpectGuestOwnedCarryover() -> None:
   carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
      [
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
            added_by_transportation=True,
            start_time=None,
            end_time=None,
         ),
      ],
      ItineraryAnimalInput(
         species='Masai Giraffe',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         is_added=True ),
      old_visit_date='2026-06-15',
   )

   assert carryover.added_by_transportation is False
   assert carryover.is_added is True
