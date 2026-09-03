from __future__ import annotations

from datetime import date

import pytest

from api.attractions.coordinators import attraction_coordinator as attraction_coordinator_module
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.attractions.data_access.attraction_hours_schedule_provider import AttractionHoursScheduleProvider
from api.attractions.data_access.attraction_provider import AttractionProvider
from api.attractions.domain.attraction_builder import AttractionBuilder
from api.attractions.scheduling.attraction_hours_schedule import AttractionHoursSchedule
from api.attractions.scheduling.attraction_hours_schedule_conflict_resolver import AttractionHoursScheduleConflictResolver
from api.attractions.scheduling.attraction_hours_schedule_time_bounds import AttractionHoursScheduleTimeBounds
from api.attractions.scheduling.attraction_hours_schedule_time_bounds_builder import AttractionHoursScheduleTimeBoundsBuilder
from api.attractions.scheduling.attraction_hours_time_bounds import AttractionHoursTimeBounds
from api.attractions.search.attractions_matching_query_builder import AttractionsMatchingQueryBuilder
from api.attractions.status.attraction_hours_schedule_status_builder import AttractionHoursScheduleStatusBuilder
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.models.attraction import Attraction
from api.types import Types


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

   assert AttractionCoordinator.get_attraction_names() == [ ATTRACTION_NAME ]


def Test_GetAttractions_TestProvidersAndBuilder_ExpectAttractions(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   attraction_records = [ object() ]
   schedule_records = [ object() ]
   override_records = [ object() ]
   captured: dict[ str, object ] = {}

   class _Context:
      target_date = VISIT_DATE

   monkeypatch.setattr(
      AttractionBuilder,
      'resolve_context',
      lambda **_kwargs: _Context() )
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

   def build_attractions( **kwargs: object ) -> list[ Attraction ]:
      captured.update( kwargs )
      return [ ATTRACTION ]

   monkeypatch.setattr( AttractionBuilder, 'build_attractions', build_attractions )

   assert AttractionCoordinator.get_attractions(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_attractions=True ) == [ ATTRACTION ]
   assert captured[ 'attraction_records' ] is attraction_records
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'include_closed_attractions' ] is True


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

   assert AttractionCoordinator.get_attractions_matching_query(
      query=QUERY,
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      include_closed_attractions=False ) == attractions


def Test_GetAttractionLikelihoodForVisitDate_TestMissingRecord_ExpectNone(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionProvider,
      'fetch_attraction_record_for_calendar_day',
      lambda *_args, **_kwargs: None )

   assert AttractionCoordinator.get_attraction_likelihood_for_visit_date(
      VISIT_DATE,
      ATTRACTION_NAME ) is None


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

   def get_likelihood_and_message( **kwargs: object ) -> tuple[ int, str | None ]:
      captured.update( kwargs )
      return 80, None

   monkeypatch.setattr(
      AttractionBuilder,
      'get_likelihood_and_message_for_date',
      get_likelihood_and_message )

   assert AttractionCoordinator.get_attraction_likelihood_for_visit_date(
      VISIT_DATE,
      ATTRACTION_NAME ) == 80
   assert captured[ 'attraction_record' ] is attraction_record
   assert captured[ 'schedule_records' ] is schedule_records
   assert captured[ 'schedule_override_records' ] is override_records
   assert captured[ 'target_date' ] == VISIT_DATE


def Test_SetAttractionAsClosed_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_as_closed(
            self,
            name: str,
            start_date: Types.DateInput,
            end_date: Types.DateInput,
            message: str ) -> bool:
         captured[ 'args' ] = ( name, start_date, end_date, message )
         return True

   monkeypatch.setattr( attraction_coordinator_module, '_mutations', StubMutations() )

   assert AttractionCoordinator.set_attraction_as_closed(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( ATTRACTION_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetAttractionClosureOverride_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_closure_override(
            self,
            name: str,
            start_date: Types.DateInput,
            end_date: Types.DateInput,
            message: str ) -> bool:
         captured[ 'args' ] = ( name, start_date, end_date, message )
         return True

   monkeypatch.setattr( attraction_coordinator_module, '_mutations', StubMutations() )

   assert AttractionCoordinator.set_attraction_closure_override(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      MESSAGE ) is True
   assert captured[ 'args' ] == ( ATTRACTION_NAME, START_DATE, END_DATE, MESSAGE )


def Test_SetAttractionOpeningSchedule_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   class StubMutations:
      def set_opening_schedule( self, *args: object ) -> bool:
         captured[ 'args' ] = args
         return True

   monkeypatch.setattr( attraction_coordinator_module, '_mutations', StubMutations() )

   assert AttractionCoordinator.set_attraction_opening_schedule(
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
      MESSAGE ) is True
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
   class StubMutations:
      def replace_opening_schedule_overlaps( self, *args: object ) -> bool:
         return args[ 0 ] == ATTRACTION_NAME

   monkeypatch.setattr( attraction_coordinator_module, '_mutations', StubMutations() )

   assert AttractionCoordinator.replace_attraction_opening_schedule_overlaps(
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
      MESSAGE ) is True


def Test_TrimAttractionOpeningScheduleOverlaps_TestMutations_ExpectDelegated(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   class StubMutations:
      def trim_opening_schedule_overlaps( self, *args: object ) -> bool:
         return args[ 0 ] == ATTRACTION_NAME

   monkeypatch.setattr( attraction_coordinator_module, '_mutations', StubMutations() )

   assert AttractionCoordinator.trim_attraction_opening_schedule_overlaps(
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
      MESSAGE ) is True


def Test_GetAttractionHoursScheduleTimeBounds_TestBuilder_ExpectBounds(
      stub_request_connection: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      AttractionHoursScheduleTimeBoundsBuilder,
      'fetch',
      lambda _conn, *, start_date=None, end_date=None: TIME_BOUNDS )

   assert AttractionCoordinator.get_attraction_hours_schedule_time_bounds(
      start_date=START_DATE,
      end_date=END_DATE ) is TIME_BOUNDS


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

   assert AttractionCoordinator.set_attraction_hours_schedule(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END ) is True
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

   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END ) is True
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

   assert AttractionCoordinator.trim_attraction_hours_schedule_overlaps(
      ATTRACTION_NAME,
      START_DATE,
      END_DATE,
      WEEKDAY_START,
      WEEKDAY_END,
      WEEKEND_START,
      WEEKEND_END ) is True
   assert saved == [ HOURS_SCHEDULE ]


def Test_GetAttractionsForSavedItinerary_TestEmptySavedAttractions_ExpectEmpty() -> None:
   assert AttractionCoordinator.get_attractions_for_saved_itinerary(
      day=VISIT_DAY,
      month=VISIT_MONTH,
      year=VISIT_YEAR,
      saved_attractions=[],
   ) == []


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
