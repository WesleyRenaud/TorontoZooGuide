from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_input import ItineraryAnimalInput
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_animal_save_carryover_mapper import ItineraryAnimalSaveCarryoverMapper
from api.shared.date_values import DateValues
from api.shared.enums.position import Position


def Test_MapFromSavedAnimalRows_TestMatchingSpeciesExhibit_ExpectScheduleCarryover() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   start_time = '2:30 PM'
   duration_minutes = 15
   end_time = DateValues.add_minutes_to_time( start_time, duration_minutes )
   saved_rows = [
      ItineraryAnimalRecord(
         species=species,
         exhibit=exhibit,
         old_likelihood=None,
         new_likelihood=100,
         start_time=start_time,
         end_time=end_time ),
   ]
   animal_input = ItineraryAnimalInput(
      species=species,
      exhibit=exhibit )
   old_visit_date = '2026-06-15'

   carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
      saved_rows,
      animal_input,
      old_visit_date=old_visit_date )

   saved_row = saved_rows[ Position.FIRST ]
   assert carryover.start_time == saved_row.start_time
   assert carryover.end_time == saved_row.end_time


def Test_MapFromSavedAnimalRows_TestNoOldVisitDate_ExpectEmptyCarryover() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   start_time = '2:30 PM'
   duration_minutes = 15
   saved_rows = [
      ItineraryAnimalRecord(
         species=species,
         exhibit=exhibit,
         old_likelihood=None,
         new_likelihood=100,
         start_time=start_time,
         end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) ),
   ]
   animal_input = ItineraryAnimalInput(
      species=species,
      exhibit=exhibit )
   old_visit_date = None

   carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
      saved_rows,
      animal_input,
      old_visit_date=old_visit_date )

   assert carryover.start_time is None
   assert carryover.end_time is None
   assert carryover.added_by_transportation is False


def Test_MapFromSavedAnimalRows_TestTransportationOwnedSavedRow_ExpectGuestOwnedCarryover() -> None:
   species = 'Masai Giraffe'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Outdoor'
   is_added = True
   saved_rows = [
      ItineraryAnimalRecord(
         species=species,
         exhibit=exhibit,
         enclosure_name=enclosure_name,
         old_likelihood=None,
         new_likelihood=100,
         added_by_transportation=True,
         start_time=None,
         end_time=None ),
   ]
   animal_input = ItineraryAnimalInput(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name,
      is_added=is_added )
   old_visit_date = '2026-06-15'

   carryover = ItineraryAnimalSaveCarryoverMapper.map_from_saved_animal_rows(
      saved_rows,
      animal_input,
      old_visit_date=old_visit_date )

   assert carryover.added_by_transportation is False
   assert carryover.is_added is animal_input.is_added
