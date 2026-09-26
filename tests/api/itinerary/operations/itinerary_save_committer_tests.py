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
from api.itinerary.domain.itinerary_adjustment import ItineraryAdjustment
from api.itinerary.domain.itinerary_adjustment_reason import ItineraryAdjustmentReason
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.operations.itinerary_save_committer import ItinerarySaveCommitter
from api.itinerary.operations.itinerary_save_context import ItinerarySaveContext
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.fixed_time_activity_rescheduler import FixedTimeActivityRescheduler
from api.itinerary.scheduling.scheduled_endpoint_visit_times_syncer import ScheduledEndpointVisitTimesSyncer
from api.models import Itinerary
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryAdjustmentType
from api.shared.enums import ItineraryErrorType, Position
from api.wild_encounters.coordinators.wild_encounter_coordinator import WildEncounterCoordinator


TURTLE_TALK = 'Nile Soft-Shelled Turtle'
RHINO_ENCOUNTER = 'Guardians of White Rhinos'
PRE_OPEN_ENCOUNTER = 'African Rainforest'
PRE_OPEN_ENCOUNTER_TIME = '8:45 AM'

CONTROLLER_KWARGS = {
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
      saved_itinerary: SavedItinerary | None = None,
      old_visit_date: str | None = None,
      adjustments: list[ ItineraryAdjustment ] | None = None,
      save_input: ItinerarySaveInput | None = None ) -> ItinerarySaveContext:
   return ItinerarySaveContext(
      conn=conn,
      save_input=save_input or ItinerarySaveInput(
         date=date( 2026, 6, 15 ),
         arrival_time='09:00',
         departure_time='17:00',
      ),
      validated_itinerary=validated_itinerary,
      current_itinerary=ItineraryBuilder.empty(),
      old_visit_date=old_visit_date,
      saved_itinerary=saved_itinerary,
      unschedule_requirements=(
         unschedule_requirements
         or ItineraryUnscheduleRequirements( talks=[], encounters=[] ) ),
      itinerary_controller_kwargs=CONTROLLER_KWARGS,
      adjustments=adjustments or [],
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


def _stub_successful_save( monkeypatch: pytest.MonkeyPatch ) -> dict[ str, object ]:
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
   return captured


@pytest.fixture
def committer_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


def Test_Commit_TestOverlappingWithoutOverride_ExpectConflictResult(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = _talk_and_encounter_validated()
   expected_names = {
      validated.guardians_talks[ Position.FIRST ].name,
      validated.wild_encounters[ Position.FIRST ].name,
   }
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ClearItineraryProvider.clear_itinerary',
      lambda conn: pytest.fail( 'save should not run on conflict' ) )

   result = ItinerarySaveCommitter.commit(
      _save_context( committer_conn, validated_itinerary=validated ),
      overriding_conflicting_guardians_talks=False )

   assert result.status == ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT
   assert len( result.reasons ) == 1
   assert {
      item.name for item in result.reasons[ Position.FIRST ].items
   } == expected_names


def Test_Commit_TestOverrideTrimsTalk_ExpectSavedWithTrimmedTalk(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
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
   talk = validated.guardians_talks[ Position.FIRST ]
   encounter = validated.wild_encounters[ Position.FIRST ]
   captured = _stub_successful_save( monkeypatch )

   result = ItinerarySaveCommitter.commit(
      _save_context( committer_conn, validated_itinerary=validated ),
      overriding_conflicting_guardians_talks=True )

   saved = captured[ 'validated_itinerary' ]
   assert isinstance( saved, ValidatedItinerary )
   assert result.status == ItineraryErrorType.SUCCESS
   assert saved.guardians_talks[ Position.FIRST ].start_time == encounter.end_time
   assert saved.guardians_talks[ Position.FIRST ].end_time == talk.end_time
   assert saved.wild_encounters[ Position.FIRST ].name == encounter.name


def Test_Commit_TestUnscheduleRequirements_ExpectAnimalSchedulesCleared(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
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
   captured = _stub_successful_save( monkeypatch )

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
   assert saved.animals[ Position.FIRST ].start_time is None
   assert saved.animals[ Position.FIRST ].end_time is None


def Test_Commit_TestNeedsReschedule_ExpectReschedulerCalled(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}
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
   monkeypatch.setattr(
      FixedTimeActivityRescheduler,
      'reschedule_after_add',
      lambda conn, **kwargs: (
         captured.__setitem__( 'reschedule_called', True )
         or ItinerarySaveResult(
            status=ItineraryErrorType.SUCCESS,
            reasons=[],
            itinerary=ItineraryBuilder.empty() ) ) )

   result = ItinerarySaveCommitter.commit(
      _save_context(
         committer_conn,
         validated_itinerary=validated,
         saved_itinerary=SavedItinerary(
            date_value='2026-06-15',
            arrival_time='9:00 AM',
            departure_time='5:00 PM',
         ) ),
      overriding_conflicting_guardians_talks=False )

   assert result.status == ItineraryErrorType.SUCCESS
   assert captured[ 'reschedule_called' ] is True


def Test_Commit_TestDateChangeNeedsReschedule_ExpectEndpointSync(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}
   visit_date = date( 2026, 6, 22 )
   old_visit_date = '2026-06-20'
   rescheduled_itinerary = ItineraryBuilder.build(
      date=visit_date.isoformat(),
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )
   saved_itinerary = SavedItinerary(
      date_value=old_visit_date,
      arrival_time='9:15 AM',
      departure_time='5:00 PM',
   )
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      needs_schedule_reschedule=True,
   )
   adjustment = ItineraryAdjustment(
      type=ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED,
      field='arrivalTime',
      previous_value=saved_itinerary.arrival_time,
      value='09:30',
      reason=ItineraryAdjustmentReason.ARRIVAL_OUTSIDE_ADMISSION_HOURS,
   )
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
      'api.itinerary.operations.itinerary_save_committer.ItinerarySaveResultBuilder.persist_walk_route',
      lambda *args, **kwargs: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_save_committer.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda *args, **kwargs: None )

   def reschedule_after_add(
         conn: sqlite3.Connection,
         *,
         saved_itinerary_before_clear: SavedItinerary | None,
         **kwargs: object ) -> ItinerarySaveResult:
      captured[ 'saved_itinerary_before_clear' ] = saved_itinerary_before_clear
      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=rescheduled_itinerary )

   def seed_if_complete( conn: sqlite3.Connection, itinerary: Itinerary ) -> None:
      captured[ 'seed_if_complete_called' ] = True

   monkeypatch.setattr(
      FixedTimeActivityRescheduler,
      'reschedule_after_add',
      reschedule_after_add )
   monkeypatch.setattr(
      ScheduledEndpointVisitTimesSyncer,
      'seed_if_complete',
      seed_if_complete )

   result = ItinerarySaveCommitter.commit(
      _save_context(
         committer_conn,
         validated_itinerary=validated,
         saved_itinerary=saved_itinerary,
         old_visit_date=old_visit_date,
         adjustments=[ adjustment ],
         save_input=ItinerarySaveInput(
            date=visit_date,
            arrival_time='09:30',
            departure_time='17:00',
         ) ),
      overriding_conflicting_guardians_talks=False )

   assert captured[ 'saved_itinerary_before_clear' ] == saved_itinerary
   assert captured[ 'seed_if_complete_called' ] is True
   assert result.adjustments[ Position.FIRST ] == adjustment
   assert result.status == ItineraryErrorType.SUCCESS


def Test_Commit_TestDateChangeDeletedTalk_ExpectSavedAsDeleted(
      committer_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='Caribou',
            exhibit='Tundra Trek',
            old_likelihood=100,
            new_likelihood=100,
            covered_by_talk=False,
            start_time='3:00 PM',
            end_time='3:03 PM',
         ),
      ],
      attractions=[],
      guardians_talks=[
         GuardiansTalkDiff(
            name='Caribou',
            is_deleted=True,
            start_time='3:00 PM',
            end_time='3:30 PM',
            location='Tundra Trek',
         ),
      ],
      wild_encounters=[
         WildEncounterDiff(
            name=RHINO_ENCOUNTER,
            is_deleted=True,
            start_time='6:00 PM',
            end_time='6:30 PM',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://example.com/rhino',
         ),
      ],
      events=[],
   )
   talk = validated.guardians_talks[ Position.FIRST ]
   encounter = validated.wild_encounters[ Position.FIRST ]
   captured = _stub_successful_save( monkeypatch )

   result = ItinerarySaveCommitter.commit(
      _save_context( committer_conn, validated_itinerary=validated ),
      overriding_conflicting_guardians_talks=False )

   saved = captured[ 'validated_itinerary' ]
   assert isinstance( saved, ValidatedItinerary )
   assert result.status == ItineraryErrorType.SUCCESS
   assert saved.guardians_talks[ Position.FIRST ].is_deleted is talk.is_deleted
   assert saved.wild_encounters[ Position.FIRST ].is_deleted is encounter.is_deleted
