from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner


def Test_IsAnimalUnscheduled_TestScheduleTimes_ExpectUnscheduledWhenIncomplete() -> None:
   assert BulkScheduleItineraryRunner.is_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
      )
   )
   assert BulkScheduleItineraryRunner.is_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='',
         end_time='',
      )
   )
   assert not BulkScheduleItineraryRunner.is_animal_unscheduled(
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         old_likelihood=None,
         new_likelihood=100,
         start_time='09:30',
         end_time='09:38',
      )
   )
