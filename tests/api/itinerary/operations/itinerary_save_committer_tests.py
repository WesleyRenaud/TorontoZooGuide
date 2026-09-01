from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.conflicts.itinerary_unschedule_requirements import ItineraryUnscheduleRequirements
from api.itinerary.data_access.itinerary_save_input import ItinerarySaveInput
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_save_committer import ItinerarySaveCommitter
from api.itinerary.operations.itinerary_save_context import ItinerarySaveContext
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.fixed_time_activity_rescheduler import FixedTimeActivityRescheduler
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


TURTLE_TALK = 'Nile Soft-Shelled Turtle'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'
PRE_OPEN_ENCOUNTER = 'African Rainforest'
PRE_OPEN_ENCOUNTER_TIME = '8:45 AM'


def _controller_kwargs() -> dict[ str, object ]:
   return {
      'animal_coordinator': AnimalCoordinator,
      'attraction_coordinator': AttractionCoordinator,
      'guardians_coordinator': GuardiansCoordinator,
      'wild_encounter_coordinator': WildEncounterCoordinator,
      'visit_date_temp': None,
   }


def _save_context(
      conn: sqlite3.Connection,
      *,
      validated_itinerary: ValidatedItinerary,
      unschedule_requirements: ItineraryUnscheduleRequirements | None = None,
      saved_itinerary: SavedItinerary | None = None ) -> ItinerarySaveContext:
   return ItinerarySaveContext(
      conn=conn,
      save_input=ItinerarySaveInput(
         date=date( 2026, 6, 15 ),
         arrival_time='09:00',
         departure_time='17:00',
      ),
      validated_itinerary=validated_itinerary,
      current_itinerary=ItineraryBuilder.empty(),
      old_visit_date=None,
      saved_itinerary=saved_itinerary,
      unschedule_requirements=(
         unschedule_requirements
         or ItineraryUnscheduleRequirements( talks=[], encounters=[] ) ),
      itinerary_controller_kwargs=_controller_kwargs(),
   )


def _talk_and_encounter_validated() -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=TURTLE_TALK,
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:30 PM',
            location='African Rainforest Pavilion' ),
      ],
      wild_encounters=[
         WildEncounterDiff(
            name=RHINO_ENCOUNTER,
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:45 PM',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://example.com/rhino' ),
      ],
      events=[],
   )


@pytest.fixture
def committer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Commit_TestOverlappingWithoutOverride_ExpectConflictResult(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ClearItineraryProvider.clear_itinerary',
      lambda conn: pytest.fail( 'save should not run on conflict' ) )

   result = ItinerarySaveCommitter.commit(
      _save_context(
         committer_conn,
         validated_itinerary=_talk_and_encounter_validated() ),
      overriding_conflicting_guardians_talks=False )

   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1
   assert { item.name for item in result.reasons[ 0 ].items } == {
      TURTLE_TALK,
      RHINO_ENCOUNTER,
   }


def Test_Commit_TestOverrideTrimsTalk_ExpectSavedWithTrimmedTalk(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ClearItineraryProvider.clear_itinerary',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.SaveItineraryProvider.save_validated_itinerary',
      lambda conn, visit_date, validated_itinerary, **kwargs: captured.__setitem__(
         'validated_itinerary',
         validated_itinerary ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveContextBuilder.current_itinerary',
      lambda conn, kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.seed_if_complete',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveResultBuilder.persist_walk_route',
      lambda *args, **kwargs: None )

   validated = ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name='African Lion',
            is_deleted=False,
            start_time='1:30 PM',
            end_time='2:00 PM',
            location='Africa Savanna' ),
      ],
      wild_encounters=[
         WildEncounterDiff(
            name='Grizzly Bear',
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:45 PM',
            meeting_spot='Wild Encounter - Americas Meeting Spot',
            link='https://example.com/grizzly' ),
      ],
      events=[],
   )

   result = ItinerarySaveCommitter.commit(
      _save_context( committer_conn, validated_itinerary=validated ),
      overriding_conflicting_guardians_talks=True )

   saved = captured[ 'validated_itinerary' ]
   assert isinstance( saved, ValidatedItinerary )
   assert result.status == ItineraryErrorType.SUCCESS
   assert saved.guardians_talks[ 0 ].start_time == '1:45 PM'
   assert saved.guardians_talks[ 0 ].end_time == '2:00 PM'
   assert saved.wild_encounters[ 0 ].name == 'Grizzly Bear'


def Test_Commit_TestUnscheduleRequirements_ExpectAnimalSchedulesCleared(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ClearItineraryProvider.clear_itinerary',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.SaveItineraryProvider.save_validated_itinerary',
      lambda conn, visit_date, validated_itinerary, **kwargs: captured.__setitem__(
         'validated_itinerary',
         validated_itinerary ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveContextBuilder.current_itinerary',
      lambda conn, kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.seed_if_complete',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveResultBuilder.persist_walk_route',
      lambda *args, **kwargs: None )

   lion = AnimalDiff(
      species='African Lion',
      exhibit='Africa Savanna',
      old_likelihood=100,
      new_likelihood=100,
      start_time='2:30 PM',
      end_time='2:45 PM' )
   validated = ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[ lion ],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name=TURTLE_TALK,
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:30 PM',
            location='African Rainforest Pavilion' ),
      ],
      wild_encounters=[],
      events=[],
   )
   requirements = ItineraryUnscheduleRequirements(
      talks=[],
      encounters=[
         WildEncounterDiff(
            name=RHINO_ENCOUNTER,
            is_deleted=False,
            start_time='2:00 PM',
            end_time='2:45 PM',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://example.com/rhino' ),
      ],
   )

   result = ItinerarySaveCommitter.commit(
      _save_context(
         committer_conn,
         validated_itinerary=validated,
         unschedule_requirements=requirements,
         saved_itinerary=SavedItinerary(
            date_value='2026-06-15',
            arrival_time='9:00 AM',
            departure_time='5:00 PM',
         ) ),
      overriding_conflicting_guardians_talks=True )

   saved = captured[ 'validated_itinerary' ]
   assert isinstance( saved, ValidatedItinerary )
   assert result.status == ItineraryErrorType.SUCCESS
   assert saved.animals[ 0 ].start_time is None
   assert saved.animals[ 0 ].end_time is None


def Test_Commit_TestNeedsReschedule_ExpectReschedulerCalled(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ClearItineraryProvider.clear_itinerary',
      lambda conn: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.SaveItineraryProvider.save_validated_itinerary',
      lambda conn, visit_date, validated_itinerary, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveContextBuilder.current_itinerary',
      lambda conn, kwargs: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.seed_if_complete',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveResultBuilder.persist_walk_route',
      lambda *args, **kwargs: None )

   def reschedule_after_add( conn: sqlite3.Connection, **kwargs: object ) -> ItinerarySaveResult:
      captured[ 'reschedule_called' ] = True
      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr(
      FixedTimeActivityRescheduler,
      'reschedule_after_add',
      reschedule_after_add )

   validated = ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      needs_schedule_reschedule=True,
   )

   ItinerarySaveCommitter.commit(
      _save_context(
         committer_conn,
         validated_itinerary=validated,
         saved_itinerary=SavedItinerary(
            date_value='2026-06-15',
            arrival_time='9:00 AM',
            departure_time='5:00 PM',
         ) ),
      overriding_conflicting_guardians_talks=False )

   assert captured[ 'reschedule_called' ] is True
