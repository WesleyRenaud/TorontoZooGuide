from __future__ import annotations

from datetime import date

from ..data_access.attraction import fetch_attraction_names
from ..data_access.attraction import fetch_attraction_record_for_calendar_day
from ..data_access.attraction import fetch_attraction_records
from ..data_access.attraction import fetch_attraction_schedule_override_records
from ..data_access.attraction import fetch_attraction_schedule_records
from ..data_access.attraction_schedule import save_attraction_opening_schedule
from ..data_access.attraction_schedule import save_attraction_schedule_override
from ...itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from ..logic.attraction import build_attractions
from ..logic.attraction import get_attraction_likelihood_and_message_for_date
from ..logic.attraction import resolve_attraction_context
from ..logic.attraction_schedule_conflict_resolution import save_attraction_opening_schedule_replacing_overlaps
from ..logic.attraction_schedule_conflict_resolution import save_attraction_opening_schedule_trimming_overlaps
from ..logic.attraction_status import build_attraction_closed_schedule
from ..logic.attraction_status import build_attraction_closure_override
from ..logic.attraction_status import build_attraction_opening_schedule
from ..logic.attractions_matching_query import build_attractions_matching_query
from ..logic.itinerary_attractions import build_itinerary_attractions
from ...models import Attraction
from ...request_connection import get_connection
from ...shared.build_amenity_coordinator_mutations import AmenityCoordinatorMutations
from ...types import DateInput, MonthInput, VisitDay, VisitYear


_mutations = AmenityCoordinatorMutations(
   build_closed_schedule=build_attraction_closed_schedule,
   build_opening_schedule=build_attraction_opening_schedule,
   build_closure_override=build_attraction_closure_override,
   save_opening_schedule=save_attraction_opening_schedule,
   save_schedule_override=save_attraction_schedule_override,
   save_replacing_overlaps=save_attraction_opening_schedule_replacing_overlaps,
   save_trimming_overlaps=save_attraction_opening_schedule_trimming_overlaps,
)


class AttractionCoordinator():
   @classmethod
   def get_attraction_names( cls ) -> list[ str ]:
      return fetch_attraction_names( get_connection() )


   @classmethod
   def get_attractions(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_attractions: bool = False ) -> list[ Attraction ]:

      context = resolve_attraction_context(
         day=day,
         month=month,
         year=year )

      return build_attractions(
         attraction_records=fetch_attraction_records(
            get_connection(),
            month=context.normalized_month,
            day=context.normalized_day ),
         schedule_records=fetch_attraction_schedule_records( get_connection() ),
         schedule_override_records=fetch_attraction_schedule_override_records(
            get_connection() ),
         context=context,
         include_closed_attractions=include_closed_attractions )


   @classmethod
   def get_attractions_for_saved_itinerary(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         saved_attractions: list[ ItineraryAttractionRecord ] ) -> list[ Attraction ]:

      if not saved_attractions:
         return []

      attractions = cls.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=True )

      return build_itinerary_attractions(
         attractions,
         saved_attractions )


   @classmethod
   def get_attractions_matching_query(
         cls,
         query: str,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear,
         include_closed_attractions: bool ) -> list[ Attraction ]:

      attractions = cls.get_attractions(
         day=day,
         month=month,
         year=year,
         include_closed_attractions=include_closed_attractions )

      return build_attractions_matching_query(
         attractions,
         query )


   @classmethod
   def get_attraction_likelihood_for_visit_date(
         cls,
         visit_date: date,
         attraction_name: str ) -> int | None:

      attraction_record = fetch_attraction_record_for_calendar_day(
         get_connection(),
         attraction_name=attraction_name,
         month=visit_date.month,
         day=visit_date.day )

      if attraction_record == None:
         return None

      likelihood, _ = get_attraction_likelihood_and_message_for_date(
         attraction_record=attraction_record,
         schedule_records=fetch_attraction_schedule_records( get_connection() ),
         schedule_override_records=fetch_attraction_schedule_override_records(
            get_connection() ),
         target_date=visit_date )

      return likelihood


   @classmethod
   def set_attraction_as_closed(
         cls,
         attraction: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      return _mutations.set_as_closed( attraction, start_date, end_date, message )


   @classmethod
   def set_attraction_closure_override(
         cls,
         attraction: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      return _mutations.set_closure_override( attraction, start_date, end_date, message )


   @classmethod
   def set_attraction_opening_schedule(
         cls,
         attraction: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return _mutations.set_opening_schedule(
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   @classmethod
   def replace_attraction_opening_schedule_overlaps(
         cls,
         attraction: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return _mutations.replace_opening_schedule_overlaps(
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )


   @classmethod
   def trim_attraction_opening_schedule_overlaps(
         cls,
         attraction: str,
         start_date: DateInput,
         end_date: DateInput,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return _mutations.trim_opening_schedule_overlaps(
         attraction,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message )
