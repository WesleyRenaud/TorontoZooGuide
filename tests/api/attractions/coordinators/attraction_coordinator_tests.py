from __future__ import annotations

from datetime import date

import pytest

from api.attractions.coordinators import attraction_coordinator as attraction_coordinator_module
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction_closure_record import AttractionClosureRecord
from api.attractions.data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from api.attractions.data_access.attraction_provider import AttractionProvider
from api.attractions.data_access.attraction_record import AttractionRecord
from api.attractions.data_access.attraction_status_provider import AttractionStatusProvider
from api.attractions.domain.attraction_builder import AttractionBuilder
from api.attractions.domain.attraction_info_link import AttractionInfoLink
from api.attractions.domain.seasonal_attraction import SeasonalAttraction
from api.attractions.domain.seasonal_attraction_builder import SeasonalAttractionBuilder
from api.attractions.scheduling.attraction_hours_schedule import AttractionHoursSchedule
from api.attractions.scheduling.attraction_hours_schedule_conflict_resolver import AttractionHoursScheduleConflictResolver
from api.attractions.scheduling.attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from api.attractions.scheduling.attraction_hours_schedule_time_bounds_builder import AttractionHoursScheduleTimeBoundsBuilder
from api.attractions.scheduling.attraction_hours_time_bounds import AttractionHoursTimeBounds
from api.attractions.search.attractions_matching_query_builder import AttractionsMatchingQueryBuilder
from api.attractions.status.attraction_hours_schedule_status_builder import AttractionHoursScheduleStatusBuilder
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.models.attraction import Attraction


VISIT_DAY = 15
VISIT_MONTH = 'June'
VISIT_YEAR = 2026
VISIT_DATE = date( 2026, 6, 15 )
ATTRACTION_NAME = 'Conservation Carousel'
CAROUSEL = 'Conservation Carousel'
GREENHOUSE = 'Greenhouse'
QUERY = 'carousel'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
MESSAGE = 'Closed for maintenance.'
WEEKDAY_START = '10:00 AM'
WEEKDAY_END = '4:00 PM'
WEEKEND_START = '9:30 AM'
WEEKEND_END = '5:00 PM'

ATTRACTION = Attraction(
   name=ATTRACTION_NAME,
   free_with_admission=True )

HOURS_SCHEDULE = AttractionHoursSchedule(
   attraction=ATTRACTION_NAME,
   start_date=START_DATE,
   end_date=END_DATE,
   weekday_start_time=WEEKDAY_START,
   weekday_end_time=WEEKDAY_END,
   weekend_holiday_start_time=WEEKEND_START,
   weekend_holiday_end_time=WEEKEND_END )

TIME_BOUNDS = AttractionHoursScheduleTimeBounds(
   weekday=AttractionHoursTimeBounds(
      open_time='9:00 AM',
      close_time='6:00 PM',
      operating_date=START_DATE ),
   weekend_holiday=AttractionHoursTimeBounds(
      open_time='9:00 AM',
      close_time='7:00 PM',
      operating_date=START_DATE ) )


class _Mutations:
   def __init__(
         self,
         captured: dict[ str, object ] | None = None,
         name: str | None = None ) -> None:
      self.captured = captured
      self.name = name


   def set_as_closed(
         self,
         name: str,
         start_date: str,
         end_date: str,
         message: str ) -> bool:
      return self._closed( name, start_date, end_date, message )


   def set_closure_override(
         self,
         name: str,
         start_date: str,
         end_date: str,
         message: str ) -> bool:
      return self._closed( name, start_date, end_date, message )


   def set_opening_schedule(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return self._opening(
         name,
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


   def replace_opening_schedule_overlaps(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return self._opening(
         name,
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


   def trim_opening_schedule_overlaps(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      return self._opening(
         name,
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


   def _closed(
         self,
         name: str,
         start_date: str,
         end_date: str,
         message: str ) -> bool:
      if self.captured != None:
         self.captured[ 'args' ] = ( name, start_date, end_date, message )
         return True

      return name == self.name


   def _opening(
         self,
         name: str,
         start_date: str,
         end_date: str,
         monday: bool,
         tuesday: bool,
         wednesday: bool,
         thursday: bool,
         friday: bool,
         saturday: bool,
         sunday: bool,
         holidays_only: bool,
         message: str ) -> bool:
      if self.captured != None:
         self.captured[ 'args' ] = (
            name,
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
         return True

      return name == self.name


class _AttractionContext:
   target_date = VISIT_DATE


def _attraction( name: str ) -> Attraction:
   return Attraction(
      name=name,
      free_with_admission=True )


def Test_GetAttractionNames_TestProviderNames_ExpectReturned(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_names',
      lambda _conn: [ ATTRACTION_NAME ] )

   attraction_names = AttractionCoordinator.get_attraction_names()

   assert attraction_names == [ ATTRACTION_NAME ]


def Test_GetAttractions_TestProvidersAndBuilder_ExpectAttractions(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attraction_records = [ object() ]
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      AttractionBuilder,
      'resolve_context',
      lambda **_kwargs: _AttractionContext() )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_records',
      lambda _conn, *, visit_date: attraction_records if visit_date == VISIT_DATE else [] )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_schedule_records',
      lambda _conn: schedule_records )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_schedule_override_records',
      lambda _conn: override_records )
   monkeypatch.setattr(
      AttractionStatusProvider,
      'fetch_closure_records',
      lambda _conn: [] )

   def build_attractions( **kwargs: object ) -> list[ Attraction ]:
      captured.update( kwargs )
      return [ ATTRACTION ]

   monkeypatch.setattr( AttractionBuilder, 'build_attractions', build_attractions )

   attractions = AttractionCoordinator.get_attractions(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_attractions=True )

   assert attractions == [ ATTRACTION ]
   assert captured[ 'attraction_records' ] is attraction_records
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'include_closed_attractions' ] is True
   assert captured[ 'closure_records' ] == []


def Test_GetAttractionsMatchingQuery_TestBuilder_ExpectMatches(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attractions = [ ATTRACTION ]

   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions',
      lambda **_kwargs: attractions )
   monkeypatch.setattr(
      AttractionsMatchingQueryBuilder,
      'build',
      lambda rows, query: rows if query == QUERY else [] )

   attractions_matching_query = AttractionCoordinator.get_attractions_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_attractions=False )

   assert attractions_matching_query == attractions


def Test_GetAttractionLikelihoodForVisitDate_TestMissingRecord_ExpectNone(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_record_for_calendar_day',
      lambda *_args, **_kwargs: None )

   attraction_likelihood_for_visit_date = AttractionCoordinator.get_attraction_likelihood_for_visit_date(
      VISIT_DATE,
      ATTRACTION_NAME )

   assert attraction_likelihood_for_visit_date is None


def Test_GetAttractionLikelihoodForVisitDate_TestPresentRecord_ExpectLikelihood(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attraction_record = object()
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_record_for_calendar_day',
      lambda *_args, **_kwargs: attraction_record )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_schedule_records',
      lambda _conn: schedule_records )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_schedule_override_records',
      lambda _conn: override_records )
   monkeypatch.setattr(
      AttractionStatusProvider,
      'fetch_closure_record',
      lambda _conn, *, attraction: None )

   def get_likelihood_and_message( **kwargs: object ) -> tuple[ int, str | None, bool ]:
      captured.update( kwargs )
      return 80, None, False

   monkeypatch.setattr(
      AttractionBuilder,
      'get_likelihood_and_message_for_date',
      get_likelihood_and_message )

   attraction_likelihood_for_visit_date = AttractionCoordinator.get_attraction_likelihood_for_visit_date(
      VISIT_DATE,
      ATTRACTION_NAME )

   assert attraction_likelihood_for_visit_date == 80
   assert captured[ 'attraction_record' ] is attraction_record
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'target_date' ] == VISIT_DATE
   assert captured[ 'closure_record' ] is None


def Test_SetAttractionAsClosed_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      attraction_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = AttractionCoordinator.set_attraction_as_closed(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == ( ATTRACTION_NAME, START_DATE, END_DATE, MESSAGE )


def Test_GetAttractionLikelihoodForVisitDate_TestActiveSeasonClosure_ExpectZero(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_record_for_calendar_day',
      lambda *_args, **_kwargs: AttractionRecord(
         name=ATTRACTION_NAME,
         free_with_admission=True,
         description='',
         info_link='',
         hyperlink_text='',
         x_coord=0,
         y_coord=0,
         region='',
         weekday_multiplier=1,
         weekend_holiday_multiplier=1 ) )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_schedule_records',
      lambda _conn: [] )
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_schedule_override_records',
      lambda _conn: [] )
   monkeypatch.setattr(
      AttractionStatusProvider,
      'fetch_closure_record',
      lambda _conn, *, attraction: AttractionClosureRecord(
         attraction=attraction,
         closed_start=START_DATE,
         closed_end=None,
         closed_message='The Conservation Carousel is closed for the season.',
         is_closed_for_season=True ) )

   attraction_likelihood_for_visit_date = AttractionCoordinator.get_attraction_likelihood_for_visit_date(
      VISIT_DATE,
      ATTRACTION_NAME )

   assert attraction_likelihood_for_visit_date == 0


def Test_SetAttractionAsClosedForSeason_TestProvider_ExpectSavedStatus(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def save_closed_for_season( _conn: str, **kwargs: object ) -> bool:
      captured.update( kwargs )
      return True

   monkeypatch.setattr(
      AttractionStatusProvider,
      'save_closed_for_season',
      save_closed_for_season )

   result = AttractionCoordinator.set_attraction_as_closed_for_season(
      ATTRACTION_NAME,
      None,
      None,
      '' )

   assert result is True
   assert captured[ 'attraction' ] == ATTRACTION_NAME
   assert captured[ 'message' ] == 'The Conservation Carousel is closed for the season.'
   assert captured[ 'end_date' ] is None


def Test_SetAttractionAsOpenForSeason_TestProvider_ExpectDeleted(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   def delete_closed_for_season( _conn: str, *, attraction: str ) -> bool:
      captured[ 'attraction' ] = attraction
      return True

   monkeypatch.setattr(
      AttractionStatusProvider,
      'delete_closed_for_season',
      delete_closed_for_season )

   result = AttractionCoordinator.set_attraction_as_open_for_season( ATTRACTION_NAME )

   assert result is True
   assert captured[ 'attraction' ] == ATTRACTION_NAME


def Test_GetClosureRecords_TestProvider_ExpectRecords(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   closure_record = AttractionClosureRecord(
      attraction=ATTRACTION_NAME,
      closed_start='2026-11-02',
      closed_end=None,
      closed_message=None,
      is_closed_for_season=True )

   monkeypatch.setattr(
      AttractionStatusProvider,
      'fetch_closure_records',
      lambda _conn: [ closure_record ] )

   records = AttractionCoordinator.get_closure_records()

   assert records == [ closure_record ]


def Test_GetSeasonalAttractions_TestClosures_ExpectBuiltAttractions(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attractions = [ AttractionInfoLink( name=ATTRACTION_NAME, info_link='https://www.torontozoo.com/tz/splash' ) ]
   closure_records = [ AttractionClosureRecord(
      attraction=ATTRACTION_NAME,
      closed_start='2026-11-02',
      closed_end=None,
      closed_message=None,
      is_closed_for_season=True,
   ) ]
   built = [ SeasonalAttraction(
      name=ATTRACTION_NAME,
      info_link='https://www.torontozoo.com/tz/splash',
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   ) ]
   captured: dict[ str, object ] = {}

   monkeypatch.setattr( AttractionCoordinator, 'get_attraction_info_links', lambda: attractions )
   monkeypatch.setattr( AttractionCoordinator, 'get_closure_records', lambda: closure_records )

   def build( **kwargs: object ) -> list[ SeasonalAttraction ]:
      captured.update( kwargs )
      return built

   monkeypatch.setattr( SeasonalAttractionBuilder, 'build', build )

   result = AttractionCoordinator.get_seasonal_attractions()

   assert result is built
   assert captured[ 'attractions' ] is attractions
   assert captured[ 'closure_records' ] is closure_records


def Test_GetClosedForSeasonAttractionNames_TestProvider_ExpectNames(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionStatusProvider,
      'fetch_closed_for_season_names',
      lambda _conn, *, today: [ ATTRACTION_NAME ] )

   names = AttractionCoordinator.get_closed_for_season_attraction_names()

   assert names == [ ATTRACTION_NAME ]


def Test_SetAttractionClosureOverride_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      attraction_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = AttractionCoordinator.set_attraction_closure_override(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == ( ATTRACTION_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetAttractionOpeningSchedule_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      attraction_coordinator_module,
      '_mutations',
      _Mutations( captured ) )

   result = AttractionCoordinator.set_attraction_opening_schedule(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE )

   assert result is True
   assert captured[ 'args' ] == (
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE )


def Test_ReplaceAttractionOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      attraction_coordinator_module,
      '_mutations',
      _Mutations( name=ATTRACTION_NAME ) )

   result = AttractionCoordinator.replace_attraction_opening_schedule_overlaps(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE )

   assert result is True


def Test_TrimAttractionOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      attraction_coordinator_module,
      '_mutations',
      _Mutations( name=ATTRACTION_NAME ) )

   result = AttractionCoordinator.trim_attraction_opening_schedule_overlaps(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      True,
      True,
      True,
      True,
      True,
      False,
      False,
      False,
      MESSAGE )

   assert result is True


def Test_GetAttractionHoursScheduleTimeBounds_TestBuilder_ExpectBounds(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'fetch',
      lambda _conn, *, start_date=None, end_date=None: TIME_BOUNDS )

   attraction_hours_schedule_time_bounds = AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
      start_date=START_DATE,
      end_date=END_DATE )

   assert attraction_hours_schedule_time_bounds is TIME_BOUNDS


def Test_SetAttractionHoursSchedule_TestWithinBounds_ExpectSaved(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ AttractionHoursSchedule ] = []

   monkeypatch.setattr(
      AttractionHoursScheduleStatusBuilder,
      'build_hours_schedule',
      lambda *_args: HOURS_SCHEDULE )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'fetch',
      lambda *_args, **_kwargs: TIME_BOUNDS )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'times_are_within_bounds',
      lambda *_args, **_kwargs: True )
   monkeypatch.setattr(
      AttractionHoursScheduleProvider,
      'save_hours_schedule',
      lambda _conn, schedule: saved.append( schedule ) or True )

   result = AttractionCoordinator.set_attraction_hours_schedule(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END )

   assert result is True
   assert saved == [ HOURS_SCHEDULE ]


def Test_SetAttractionHoursSchedule_TestOutsideBounds_ExpectValueError(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionHoursScheduleStatusBuilder,
      'build_hours_schedule',
      lambda *_args: HOURS_SCHEDULE )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'fetch',
      lambda *_args, **_kwargs: TIME_BOUNDS )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'times_are_within_bounds',
      lambda *_args, **_kwargs: False )

   with pytest.raises( ValueError, match='Attraction hours must fall within regular zoo hours' ):
      AttractionCoordinator.set_attraction_hours_schedule(
         ATTRACTION_NAME,
         START_DATE,
         END_DATE,
         WEEKDAY_START,
         WEEKDAY_END,
         WEEKEND_START,
         WEEKEND_END )


def Test_ReplaceAttractionHoursScheduleOverlaps_TestResolver_ExpectCalled(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ AttractionHoursSchedule ] = []

   monkeypatch.setattr(
      AttractionHoursScheduleStatusBuilder,
      'build_hours_schedule',
      lambda *_args: HOURS_SCHEDULE )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'fetch',
      lambda *_args, **_kwargs: TIME_BOUNDS )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'times_are_within_bounds',
      lambda *_args, **_kwargs: True )
   monkeypatch.setattr(
      AttractionHoursScheduleConflictResolver,
      'save_replacing_overlaps',
      lambda _conn, schedule: saved.append( schedule ) or True )

   result = AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END )

   assert result is True
   assert saved == [ HOURS_SCHEDULE ]


def Test_TrimAttractionHoursScheduleOverlaps_TestResolver_ExpectCalled(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   saved: list[ AttractionHoursSchedule ] = []

   monkeypatch.setattr(
      AttractionHoursScheduleStatusBuilder,
      'build_hours_schedule',
      lambda *_args: HOURS_SCHEDULE )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'fetch',
      lambda *_args, **_kwargs: TIME_BOUNDS )
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'times_are_within_bounds',
      lambda *_args, **_kwargs: True )
   monkeypatch.setattr(
      AttractionHoursScheduleConflictResolver,
      'save_trimming_overlaps',
      lambda _conn, schedule: saved.append( schedule ) or True )

   result = AttractionCoordinator.trim_attraction_hours_schedule_overlaps(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END )

   assert result is True
   assert saved == [ HOURS_SCHEDULE ]


def Test_GetAttractionsForSavedItinerary_TestEmptySavedAttractions_ExpectEmpty() -> None:
   attractions_for_saved_itinerary = AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_attractions=[],
   )

   assert attractions_for_saved_itinerary == []


def Test_GetAttractionsForSavedItinerary_TestSavedAttractions_ExpectBuilderFilteredAttractions(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attractions = [
      _attraction( GREENHOUSE ),
      _attraction( CAROUSEL ),
      _attraction( 'Tundra Air' ),
   ]
   captured: dict[ str, object ] = {}

   def get_attractions( **kwargs: object ) -> list[ Attraction ]:
      captured[ 'kwargs' ] = kwargs
      return attractions

   monkeypatch.setattr(
      AttractionCoordinator,
      'get_attractions',
      get_attractions )

   saved_attractions = [
      ItineraryAttractionRecord(
         attraction=GREENHOUSE,
         old_likelihood=None,
         new_likelihood=None ),
      ItineraryAttractionRecord(
         attraction=CAROUSEL,
         old_likelihood=None,
         new_likelihood=None ),
   ]

   result = AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_attractions=saved_attractions,
   )

   assert captured[ 'kwargs' ] == {
      'day': VISIT_DAY,
      'month': VISIT_MONTH,
      'year': VISIT_YEAR,
      'include_closed_attractions': True,
   }
   assert [ attraction.name for attraction in result ] == [ CAROUSEL, GREENHOUSE ]
