from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.scheduling.bulk.loop_unit_schedule_persist_error import LoopUnitSchedulePersistError


LION = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   old_likelihood=None,
   new_likelihood=100,
)


def Test_Init_TestStops_ExpectStopsAttached() -> None:
   error = LoopUnitSchedulePersistError( [ LION ] )

   assert error.stops == [ LION ]
