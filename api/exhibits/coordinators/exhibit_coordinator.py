from __future__ import annotations

from ..data_access.exhibit import fetch_animal_names_in_exhibit
from ..data_access.exhibit import fetch_exhibit_names
from ..data_access.exhibit import fetch_exhibit_names_in_region
from ..data_access.exhibit import fetch_region_exhibit_rows
from ..data_access.exhibit_closure import fetch_exhibit_closure_records
from ..data_access.exhibit_closure import save_exhibit_closed_status
from ..data_access.exhibit_closure import save_exhibit_open_status
from ..domain.exhibit import build_region_options
from ..domain.regions_with_exhibits import build_regions_with_exhibits
from ...models import Region
from ...models import RegionWithExhibits
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ..status.exhibit_closure import exhibit_names_closed_on_visit_date
from ..status.exhibit_status import build_exhibit_closed_status
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class ExhibitCoordinator():
   @classmethod
   def get_exhibits_in_region( cls, region: str ) -> list[ str ]:
      return fetch_exhibit_names_in_region(
         get_connection(),
         region=region )


   @classmethod
   def get_exhibits( cls ) -> list[ str ]:
      return fetch_exhibit_names( get_connection() )


   @classmethod
   def get_regions( cls ) -> list[ Region ]:
      return build_region_options(
         fetch_region_exhibit_rows( get_connection() ) )


   @classmethod
   def get_regions_with_exhibits( cls ) -> list[ RegionWithExhibits ]:
      return build_regions_with_exhibits(
         fetch_region_exhibit_rows( get_connection() ) )


   @classmethod
   def get_names_of_animals_in_exhibit( cls, exhibit: str ) -> list[ str ]:
      return fetch_animal_names_in_exhibit(
         get_connection(),
         exhibit=exhibit )


   @classmethod
   def get_closed_exhibits_for_visit_date(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ str ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      return exhibit_names_closed_on_visit_date(
         fetch_exhibit_closure_records( get_connection() ),
         target_date )


   @classmethod
   def set_exhibit_as_closed(
         cls,
         exhibit: str,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> bool:
      status = build_exhibit_closed_status(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return save_exhibit_closed_status(
         get_connection(),
         exhibit=status.exhibit,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_exhibit_as_open(
         cls,
         exhibit: str,
         start_date: DateInput,
         end_date: DateInput ) -> bool:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return save_exhibit_open_status(
         get_connection(),
         exhibit=exhibit,
         start_date=date_range.start_date,
         end_date=date_range.end_date )
