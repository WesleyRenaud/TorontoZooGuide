from __future__ import annotations

from ..data_access.exhibit_provider import ExhibitProvider
from ..data_access.exhibit_status_provider import ExhibitStatusProvider
from ..domain.region_options_builder import RegionOptionsBuilder
from ..domain.regions_with_exhibits_builder import RegionsWithExhibitsBuilder
from ...models import Region
from ...models import RegionWithExhibits
from ...request_connection_provider import RequestConnectionProvider
from ...shared.calendar_dates import CalendarDates
from ...shared.calendar_dates import DateValues
from ..status.exhibit_status_builder import ExhibitStatusBuilder
from ...types import Types


class ExhibitCoordinator():
   @classmethod
   def get_exhibits_in_region( cls, region: str ) -> list[ str ]:
      return ExhibitProvider.fetch_exhibit_names_in_region(
         RequestConnectionProvider.get(),
         region=region )


   @classmethod
   def get_exhibits( cls ) -> list[ str ]:
      return ExhibitProvider.fetch_exhibit_names( RequestConnectionProvider.get() )


   @classmethod
   def get_regions( cls ) -> list[ Region ]:
      return RegionOptionsBuilder.build(
         ExhibitProvider.fetch_region_exhibit_rows( RequestConnectionProvider.get() ) )


   @classmethod
   def get_regions_with_exhibits( cls ) -> list[ RegionWithExhibits ]:
      return RegionsWithExhibitsBuilder.build(
         ExhibitProvider.fetch_region_exhibit_rows( RequestConnectionProvider.get() ) )


   @classmethod
   def get_names_of_animals_in_exhibit( cls, exhibit: str ) -> list[ str ]:
      return ExhibitProvider.fetch_animal_names_in_exhibit(
         RequestConnectionProvider.get(),
         exhibit=exhibit )


   @classmethod
   def get_closed_exhibits_for_visit_date(
         cls,
         month: Types.MonthInput,
         day: Types.VisitDay,
         year: Types.VisitYear ) -> list[ str ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      return ExhibitStatusBuilder.exhibit_names_closed_on_visit_date(
         ExhibitStatusProvider.fetch_closure_records( RequestConnectionProvider.get() ),
         target_date )


   @classmethod
   def set_exhibit_as_closed(
         cls,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      status = ExhibitStatusBuilder.build_closed_status(
         exhibit=exhibit,
         start_date=start_date,
         end_date=end_date,
         message=message )

      return ExhibitStatusProvider.save_closed_status(
         RequestConnectionProvider.get(),
         exhibit=status.exhibit,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message )


   @classmethod
   def set_exhibit_as_open(
         cls,
         exhibit: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return ExhibitStatusProvider.save_open_status(
         RequestConnectionProvider.get(),
         exhibit=exhibit,
         start_date=date_range.start_date,
         end_date=date_range.end_date )
