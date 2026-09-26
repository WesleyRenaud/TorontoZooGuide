from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_save_committer import ItinerarySaveCommitter
from api.itinerary.operations.itinerary_save_context import ItinerarySaveContext
from api.itinerary.operations.itinerary_save_warning_checker import ItinerarySaveWarningChecker
from api.itinerary.operations.itinerary_save_zoo_hours_validator import ItinerarySaveZooHoursValidator
from api.itinerary.operations.itinerary_setter import ItinerarySetter
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


SUCCESS_RESULT = ItinerarySaveResult(
   status=ItineraryErrorType.SUCCESS,
   reasons=[],
   itinerary=ItineraryBuilder.empty() )

WARNING_RESULT = ItinerarySaveResult(
   status=ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
   reasons=[],
   itinerary=ItineraryBuilder.empty() )

ZOO_HOURS_ERROR = ItinerarySaveResult(
   status=ItineraryErrorType.TIME_OUT_OF_BOUNDS,
   reasons=[],
   itinerary=ItineraryBuilder.empty() )

VISIT_DATE = date( 2026, 6, 22 )
OLD_VISIT_DATE = '2026-06-20'
ARRIVAL_TIME = '09:30'
DEPARTURE_TIME = '17:00'


def _save_context( conn: sqlite3.Connection ) -> ItinerarySaveContext:
   return ItinerarySaveContext(
      conn=conn,
      save_input=ItinerarySaveInput(
         date=VISIT_DATE,
         arrival_time=ARRIVAL_TIME,
         departure_time=DEPARTURE_TIME,
      ),
      validated_itinerary=object(),
      current_itinerary=ItineraryBuilder.empty(),
      old_visit_date=OLD_VISIT_DATE,
      saved_itinerary=None,
      unschedule_requirements=object(),
      itinerary_controller_kwargs={} )


@pytest.fixture
def setter_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Set_TestZooHoursError_ExpectEarlyReturnWithoutCommit(
      setter_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItineraryProvider.fetch_itinerary_date',
      lambda conn: OLD_VISIT_DATE )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItinerarySaveRestrictiveHoursAdjuster.adjust',
      lambda conn, save_input, **kwargs: ( save_input, [] ) )
   monkeypatch.setattr(
      ItinerarySaveZooHoursValidator,
      'validate',
      lambda conn, save_input, controller_kwargs: ZOO_HOURS_ERROR )
   monkeypatch.setattr(
      ItinerarySaveCommitter,
      'commit',
      lambda *args, **kwargs: pytest.fail( 'commit should not run on zoo hours error' ) )

   result = ItinerarySetter.set(
      setter_conn,
      VISIT_DATE.isoformat(),
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False )

   assert result == ZOO_HOURS_ERROR


def Test_Set_TestSaveWarning_ExpectEarlyReturnWithoutCommit(
      setter_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   save_context = _save_context( setter_conn )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItineraryProvider.fetch_itinerary_date',
      lambda conn: OLD_VISIT_DATE )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItinerarySaveRestrictiveHoursAdjuster.adjust',
      lambda conn, save_input, **kwargs: ( save_input, [] ) )
   monkeypatch.setattr(
      ItinerarySaveZooHoursValidator,
      'validate',
      lambda conn, save_input, controller_kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItinerarySaveContextPreparer.prepare',
      lambda conn, save_input, **kwargs: save_context )
   monkeypatch.setattr(
      ItinerarySaveWarningChecker,
      'check',
      lambda context, **kwargs: ( context, WARNING_RESULT ) )
   monkeypatch.setattr(
      ItinerarySaveCommitter,
      'commit',
      lambda *args, **kwargs: pytest.fail( 'commit should not run when warning is returned' ) )

   result = ItinerarySetter.set(
      setter_conn,
      VISIT_DATE.isoformat(),
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_guardians_talk_unschedule=False,
      confirming_wild_encounter_unschedule=False )

   assert result == WARNING_RESULT


def Test_Set_TestValidSave_ExpectCommitCalled(
      setter_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   save_context = _save_context( setter_conn )
   commit_calls: list[ object ] = []
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItineraryProvider.fetch_itinerary_date',
      lambda conn: OLD_VISIT_DATE )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItinerarySaveRestrictiveHoursAdjuster.adjust',
      lambda conn, save_input, **kwargs: ( save_input, [] ) )
   monkeypatch.setattr(
      ItinerarySaveZooHoursValidator,
      'validate',
      lambda conn, save_input, controller_kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_setter.ItinerarySaveContextPreparer.prepare',
      lambda conn, save_input, **kwargs: save_context )
   monkeypatch.setattr(
      ItinerarySaveWarningChecker,
      'check',
      lambda context, **kwargs: ( context, None ) )
   monkeypatch.setattr(
      ItinerarySaveCommitter,
      'commit',
      lambda context, **kwargs: commit_calls.append( context ) or SUCCESS_RESULT )

   result = ItinerarySetter.set(
      setter_conn,
      VISIT_DATE.isoformat(),
      ARRIVAL_TIME,
      DEPARTURE_TIME,
      animal_coordinator=AnimalCoordinator,
      attraction_coordinator=AttractionCoordinator,
      guardians_coordinator=GuardiansCoordinator,
      wild_encounter_coordinator=WildEncounterCoordinator,
      confirming_guardians_talk_unschedule=True,
      confirming_wild_encounter_unschedule=True,
      overriding_conflicting_guardians_talks=True )

   assert result == SUCCESS_RESULT
   assert commit_calls == [ save_context ]
